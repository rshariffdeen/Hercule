import filetype
import os
import re
from os.path import join
from git import Repo
from app.core import utilities, emitter, values
from app.tools import archives



def extract_file_types(dir_path):
    file_types = dict()
    file_list = utilities.get_file_list(dir_path)
    for f_p in file_list:
        if not f_p:
            continue
        kind = filetype.guess(f_p)
        if kind is None:
            kind = utilities.execute_command(f"file --brief {f_p}")[1].decode().split(",")[0].strip()
        else:
            kind = kind.extension
        if kind not in file_types:
            file_types[kind] = list()
        file_types[kind].append(str(f_p).replace(dir_path, ""))
    return file_types


def extract_compiled_python(dir_path):
    emitter.normal("\t\tfinding compiled python files")
    file_list = utilities.get_file_list(dir_path)
    compiled_python2_list = []
    compiled_python3_list = []
    for f_p in file_list:
        if not f_p:
            continue
        kind = filetype.guess(f_p)
        if kind is None:
            kind = utilities.execute_command(f"file --brief {f_p}")[1].decode().split(",")[0].strip()
        else:
            kind = kind.extension
        if "python 2" in kind and "byte-compiled" in kind:
            compiled_python2_list.append(f_p)
        if "python 3" in kind and "byte-compiled" in kind:
            compiled_python3_list.append(f_p)
    return compiled_python2_list, compiled_python3_list


def extract_source(source_url, github_page, dir_src, pkg_version):
    emitter.sub_title("Extracting Source")
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
                if pkg_version.strip().lower() in str(t).strip().lower():
                    release_tag = t
                    break
            emitter.highlight(f"\t\t\t release tag: {release_tag}")
            repo.git.checkout(release_tag)
    else:
        emitter.normal("\t\tcache found, skipping fetch")


def extract_meta_data(dir_pkg):
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

    return package_name, package_version, source_url, github_page


def extract_archive(pkg_path):
    emitter.sub_title("Extracting Files")
    emitter.sub_sub_title("extracting original compressed file")
    archive_path = str(pkg_path)
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
    return dir_pkg
