import os.path
import json
from os.path import join
import csv
from typing import Any
import sys


def write_as_csv(data: Any, output_file_path: str):
    with open(output_file_path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        for output in data:
            writer.writerow(output)


def read_json(file_path: str):
    json_data = None
    if os.path.isfile(file_path):
        with open(file_path, "r") as in_file:
            content = in_file.readlines()
            if len(content) == 1:
                content = content[0]
            else:
                content_str = " ".join([l.strip().replace("\n", "") for l in content])
                content = content_str
            json_data = json.loads(content)

    return json_data


def run(sym_args):
    if not sym_args:
        print("requires the path to the dir and the pkg name list")
        exit(1)
    dir_path = sym_args[0]
    pkg_list = sym_args[1]
    if not os.path.isdir(dir_path):
        print("path is invalid", dir_path)
        exit(1)
    if not os.path.isfile(pkg_list):
        print("path is invalid", pkg_list)
        exit(1)

    aggregated_data = []
    list_packages = [f for f in os.listdir(dir_path) if os.path.isfile(join(dir_path, f)) and
                     ".json" not in f and ".txt" not in f]
    filtered_pkg_list = []
    with open(pkg_list, "r") as _f:
        content = _f.readlines()
        filtered_pkg_list = [f.strip().replace("\n", "") for f in content]

    print(dir_path, len(list_packages))
    for pkg_name in list_packages:
        if pkg_name not in filtered_pkg_list:
            continue
        print(pkg_name)
        report_name = f"{pkg_name}.json"
        report_path = f"{dir_path}/{report_name}"
        pkg_path = f"{dir_path}/{pkg_name}"
        if not os.path.isfile(report_path):
            print(pkg_name)
            scan_command = f"guarddog pypi scan {pkg_path} --output-format=json > {report_path}"
            print(scan_command)
            os.system(scan_command)
        json_report = read_json(str(report_path))
        print(report_path)
        aggregated_data.append((json_report["package"], json_report["issues"], json_report["errors"], json_report["results"]))

    write_as_csv(aggregated_data, f"{dir_path}/aggregated_data.csv")


if __name__ == "__main__":
    run(sys.argv[1:])
