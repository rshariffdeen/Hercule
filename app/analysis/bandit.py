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
            if len(content) > 1:
                content_str = " ".join([l.strip().replace("\n", "") for l in content])
                content = content_str
            json_data = json.loads(content)
    return json_data

def run_bandit(dir_path):
    curr_dir = os.getcwd()
    dir_name = dir_path.split("/")[-1]
    os.chdir(os.path.dirname(dir_path))
    report_file = f"{dir_name}.json"
    if not os.path.isfile(report_file):
        os.system(f"bandit -r {dir_name} -lll -f json -o {dir_name}.json")
    analysis_data = read_json(report_file)
    no_errors = 0
    if analysis_data["errors"]:
        no_errors = len(analysis_data["errors"])
    no_high = analysis_data["metrics"]["_totals"]["SEVERITY.HIGH"]
    no_medium = analysis_data["metrics"]["_totals"]["SEVERITY.MEDIUM"]
    no_low = analysis_data["metrics"]["_totals"]["SEVERITY.LOW"]
    no_undefined = analysis_data["metrics"]["_totals"]["SEVERITY.UNDEFINED"]
    os.chdir(curr_dir)
    return no_high, no_medium, no_low, no_undefined, no_errors

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
            dir_name = f"{f_name}-dir"
            dir_path = join(dir_pkg, dir_name)
            file_path = join(dir_pkg, f_name)
            file_extension = f_name.split(".")[-1]
            try:
                if file_extension in ["conda", "whl"]:
                    os.system(f"unzip {file_path} -d {dir_path}")
                if file_extension in ["gz", "bz2"]:
                    os.system(f"mkdir -p {dir_path}")
                    os.system(f"tar -xf {file_path} -C {dir_path}")
                if file_extension in ["json"]:
                    continue
            except Exception as ex:
                print("not supported archive", file_extension, f_name)
                continue
            result = run_bandit(dir_path)
            output_content.append((f_name, result[0], result[1], result[2], result[3], result[4]))

        if output_content:
            sorted_content = sorted(output_content, key=lambda x:x[0])
            write_as_csv(sorted_content, f"{pkg_name}-bandit.csv")

if __name__ == "__main__":
    run(sys.argv[1:])
