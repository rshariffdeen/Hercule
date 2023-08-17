import os.path
import re
from os.path import join
from bs4 import BeautifulSoup
import requests
import csv
import ssl
import sys
from typing import Any
import tarfile
import sys
from contextlib import closing
from zipfile import ZipFile


def extract_versions(f_name, pkg_name):
    pkg_regex = fr'{pkg_name}-([0-9.]*)'
    py_regex = r'py([0-9]+)'
    pkg_version = f_name
    pkg_v_result = re.search(pkg_regex, f_name)
    if pkg_v_result:
        pkg_version = pkg_v_result.group(1)
    py_version = f_name
    py_v_result = re.search(py_regex, f_name)
    if py_v_result:
        py_version = py_v_result.group(1)

    os_version = "unknown"
    if "windows" in f_name.lower() or "win" in f_name.lower():
        os_version = "windows"
    elif "linux" in f_name.lower():
        os_version = "linux"
    elif "osx" in f_name.lower() or "ios" in f_name.lower():
        os_version = "osx"
    return pkg_version, py_version, os_version


def write_as_csv(data: Any, output_file_path: str):
    with open(output_file_path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        for output in data:
            writer.writerow(output)

def run(sym_args):
    if not sym_args:
        print("requires the path to the dir")
        exit(1)
    download_dir = sym_args[0]
    if not os.path.isdir(download_dir):
        print("path is invalid", download_dir)
        exit(1)

    list_packages = [d for d in os.listdir(download_dir) if os.path.isdir(join(download_dir, d))]
    for pkg_name in list_packages:
        output_content = []
        dir_pkg = os.path.join(download_dir, pkg_name)
        file_list = [f for f in os.listdir(dir_pkg) if os.path.isfile(join(dir_pkg, f))]
        for f_name in file_list:
            pkg_v, py_v, os_v = extract_versions(f_name, pkg_name)
            file_extension = f_name.split(".")[-1]
            file_size = os.stat(join(dir_pkg, f_name)).st_size
            file_count = 0
            try:
                if file_extension in ["conda", "whl"]:
                    with closing(ZipFile(join(dir_pkg, f_name))) as archive:
                        file_count = len(archive.infolist())
                if file_extension in ["gz", "bz2"]:
                    with tarfile.open(join(dir_pkg, f_name)) as archive:
                        file_count = sum(1 for member in archive if member.isreg())
                if file_extension in ["json"]:
                    continue
            except Exception as ex:
                print("not supported extension", file_extension)
            output_content.append((f_name, pkg_v, py_v, os_v, file_extension, file_size, file_count))
        if output_content:
            write_as_csv(output_content, f"{pkg_name}-meta-data.csv")

if __name__ == "__main__":
    run(sys.argv[1:])
