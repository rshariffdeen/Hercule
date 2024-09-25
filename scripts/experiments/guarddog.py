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
        print("requires the path to the dir")
        exit(1)
    download_dir = sym_args[0]
    if not os.path.isdir(download_dir):
        print("path is invalid", download_dir)
        exit(1)

    aggregated_data = []
    list_packages = [f for f in os.listdir(download_dir) if os.path.isfile(join(download_dir, f))]
    for pkg_name in list_packages:
        report_name = f"{pkg_name}.json"
        report_path = f"{os.getcwd()}/{report_name}"
        pkg_path = f"{download_dir}/{pkg_name}"
        if not os.path.isfile(report_path):
            print(pkg_name)
            scan_command = f"guarddog pypi scan {pkg_path} --output-format=json > {report_path}"
            print(scan_command)
            os.system(scan_command)
        print(report_name)
        aggregated_data.append(read_json(str(report_path)))

    write_as_csv(aggregated_data, "aggregated_data.csv")


if __name__ == "__main__":
    run(sys.argv[1:])
