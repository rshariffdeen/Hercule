import os
import re
import signal
import sys
import time
import filetype
import traceback
from argparse import Namespace
from multiprocessing import set_start_method
from git import Repo

from typing import Any
from typing import Dict
from typing import List
from os.path import join
import rich.traceback
import yaml
from rich import get_console

from app.core import configuration
from app.core import definitions
from app.core import decompile
from app.core import emitter
from app.core import logger
from app.core import utilities
from app.core import values
from app.core import analysis
from app.tools import archives
from app.core.args import parse_args
from app.core.configuration import Configurations
from app.notification import notification


def create_output_directories():
    dir_list = [
        values.dir_logs,
        values.dir_output_base,
        values.dir_log_base,
        values.dir_results,
        values.dir_experiments,
    ]

    for dir_i in dir_list:
        if not os.path.isdir(dir_i):
            os.makedirs(dir_i)


def timeout_handler(signum, frame):
    emitter.error("TIMEOUT Exception")
    raise Exception("end of time")


def shutdown(signum, frame):
    # global stop_event
    emitter.warning("Exiting due to Terminate Signal")
    # stop_event.set()
    raise SystemExit


def bootstrap(arg_list: Namespace):
    emitter.sub_title("Bootstrapping framework")
    config = Configurations()
    config.read_email_config_file()
    config.read_slack_config_file()
    config.read_discord_config_file()
    config.read_arg_list(arg_list)
    values.is_arg_valid = True
    config.update_configuration()
    config.print_configuration()


def run(parsed_args):
    package_path = parsed_args.file
    emitter.sub_title("Extracting Files")
    emitter.sub_sub_title("extracting original compressed file")
    archive_path = str(package_path.name)
    archive_name = str(archive_path).split("/")[-1]
    file_extension = archive_name.split(".")[-1]
    dir_pkg = f"{values.dir_experiments}/{archive_name}-dir"
    extract_dir = archives.decompress_archive(archive_path, file_extension, dir_pkg)
    emitter.sub_sub_title("extracting internally compressed file(s)")
    archive_list = archives.find_compressed(extract_dir)
    emitter.highlight(f"\t\t\tArchive File Count: {len(archive_list)}")
    for a_f in archive_list:
        archive_name = str(a_f).split("/")[-1]
        file_extension = archive_name.split(".")[-1]
        d_path = f"{a_f}-dir"
        archives.decompress_archive(str(a_f), file_extension, d_path)

    emitter.sub_title("Searching Meta Data")
    emitter.sub_sub_title("finding for meta-data files")
    meta_data_files = ["meta.yaml", "METADATA", "about.json", "index.json", "PKG-INFO"]
    source_url = None
    package_version = None
    package_name = None
    github_page = None
    for f_name in meta_data_files:
        result_list = utilities.find_file(dir_pkg, f_name)
        if result_list:
            for f_path in result_list:
                if not f_path:
                    continue
                emitter.normal(f"\t\t found {f_path}")
                abs_path = join(dir_pkg, f_path)
                if "yaml" in f_name:
                    meta_data = utilities.read_yaml(abs_path)
                    meta_data_file = f_path
                    if "source" in meta_data:
                        source_url = meta_data["source"]["url"]
                    if "package" in meta_data:
                        package_name = meta_data["package"]["name"].strip()
                        package_version = meta_data["package"]["version"].strip()
                elif "json" in f_name:
                    meta_data = utilities.read_json(abs_path)
                    meta_data_file = f_path
                    if "home" in meta_data:
                        home_url = meta_data["home"]
                        if "github.com" in home_url:
                            github_page = home_url
                    if "version" in meta_data:
                        package_version = meta_data["version"].strip()
                    if "name" in meta_data:
                        package_name = meta_data["name"]
                elif "PKG-INFO" in f_name:
                    meta_info = utilities.read_file(abs_path)
                    for l in meta_info:
                        if "Name: " in l:
                            package_name = l.split(": ")[-1].strip()
                        elif "Version: " in l:
                            package_version = l.split(": ")[-1].strip()
                        elif "Home-page:" in l:
                            home_url = l.split(": ")[-1]
                            if "github.com" in home_url:
                                github_page = home_url
                                break
                        elif "github.com" in l:
                            result = re.search(r"//(.*?).git", l)
                            if result:
                                github_repo = result.group(1)
                                github_page = f"https://{github_repo}.git"
                                break
                else:
                    meta_info = utilities.read_file(abs_path)
                    for l in meta_info:
                        if "Name: " in l:
                            package_name = l.split(": ")[-1].strip()
                        elif "Version: " in l:
                            package_version = l.split(": ")[-1].strip()
                        elif "Home-page:" in l:
                            home_url = l.split(": ")[-1]
                            if "github.com" in home_url:
                                github_page = home_url
                                break

            if source_url and package_version and package_name:
                break
            if github_page and package_name and package_version:
                break

    if not source_url and not github_page:
        utilities.error_exit("failed to identify source")

    emitter.highlight(f"\t\t\t package name: {package_name}")
    emitter.highlight(f"\t\t\t package version: {package_version}")
    emitter.highlight(f"\t\t\t package source: {source_url}")
    emitter.highlight(f"\t\t\t package github: {github_page}")

    emitter.sub_title("Fetching Source")
    dir_src = dir_pkg.replace("-dir", "-src")
    if not os.path.isdir(dir_src):
        if source_url:
            emitter.sub_sub_title("downloading from URL")
            release_file = os.path.dirname(dir_src) + "/src-archive"
            utilities.download_file(source_url, release_file)
            file_type = filetype.guess(release_file)
            if not file_type:
                utilities.error_exit(f"unknown release file type {release_file}")
            file_ext = file_type.extension
            archives.decompress_archive(release_file, file_ext, dir_src)
        elif github_page:
            emitter.sub_sub_title("cloning from github")
            emitter.normal("\t\tfetching code")
            repo = Repo.clone_from(github_page, dir_src)
            emitter.highlight(f"\t\t\t fetched dir: {dir_src}")
            tag_list = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            emitter.normal("\t\tfinding release tag")
            release_tag = None
            for t in tag_list:
                if package_version.strip().lower() in str(t).strip().lower():
                    release_tag = t
                    break
            emitter.highlight(f"\t\t\t release tag: {release_tag}")
            repo.git.checkout(release_tag)
    else:
        emitter.normal("\t\tcache found, skipping fetch")

    analysis.analyze_file_types(dir_pkg, dir_src)
    decompile.decompile_python_files(dir_pkg, dir_src)


def main():
    if not sys.warnoptions:
        import warnings

        warnings.simplefilter("ignore")

    rich.traceback.install(show_locals=True)
    parsed_args = parse_args()
    is_error = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.signal(signal.SIGTERM, shutdown)
    set_start_method("spawn")
    start_time = time.time()
    create_output_directories()
    logger.create_log_files()
    # TODO Do overwrite magic
    bootstrap(parsed_args)
    try:
        emitter.title(
            "Starting {} (Supply Chain Detector) ".format(values.tool_name)
        )
        if not parsed_args.file:
            utilities.error_exit(
                "Package was not found. Please make sure file exist"
            )
        else:
            run(parsed_args)
    except (SystemExit, KeyboardInterrupt) as e:
        pass
    except Exception as e:
        is_error = True
        values.ui_active = False
        emitter.error("Runtime Error")
        emitter.error(str(e))
        logger.error(traceback.format_exc())
    finally:
        get_console().show_cursor(True)
        # Final running time and exit message
        # os.system("ps -aux | grep 'python' | awk '{print $2}' | xargs kill -9")
        total_duration = format((time.time() - start_time) / 60, ".3f")
        notification.end(total_duration, is_error)
        emitter.end(total_duration, is_error)
