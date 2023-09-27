import os
import re
import signal
import sys
import time
import pathlib
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
from app.core import extract
from app.core import writer
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


def scan_package(package_path):
    emitter.sub_title(package_path)
    start_time = time.time()
    values.result = dict()
    values.result["general"] = dict()
    dir_pkg = extract.extract_archive(package_path)
    package_name, package_version, source_url, github_page = extract.extract_meta_data(dir_pkg)
    distribution_name = dir_pkg.split("/")[-1].replace("-dir", "")
    values.result["package-name"] = package_name
    values.result["file-name"] = distribution_name
    values.result["version"] = package_version
    values.result["source-url"] = source_url
    values.result["github-page"] = github_page
    dir_src = dir_pkg.replace("-dir", "-src")
    if github_page or source_url:
        is_success = extract.extract_source(source_url, github_page, dir_src, package_version)
        if is_success:
            analysis.analyze_files(dir_pkg, dir_src)
    time_duration = format((time.time() - start_time) / 60, ".3f")
    values.result["scan-duration"] = time_duration
    result_file_name = join(values.dir_results, f"{distribution_name}.json")
    min_result_file_name = join(values.dir_results, f"{distribution_name}.min.json")
    writer.write_as_json(values.result, result_file_name)
    del values.result["bandit-analysis"]["hercule-report"]
    del values.result["suspicious-modifications"]
    writer.write_as_json(values.result, min_result_file_name)


def run(parsed_args):
    if parsed_args.file:
        package_path = parsed_args.file.name
        scan_package(package_path)
    elif parsed_args.dir:
        list_packages = utilities.list_dir(parsed_args.dir)
        for _pkg in list_packages:
            if os.path.isfile(_pkg):
                scan_package(_pkg)


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
        if not parsed_args.file and not parsed_args.dir:
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

