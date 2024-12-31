import os.path
import json
from os.path import join
import csv
from typing import Any
import sys
from multiprocessing import Pool
from os.path import join


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


def is_flagged(file_path: str):
    with open(file_path, "r") as f:
        contents = f.read()
        return "api_results {" in contents


def process(data):
    pkg_name, dir_path, output_dir = data
    print(pkg_name)
    pkg_path = f"{dir_path}/{pkg_name}"
    final_output = join("/opt/maloss/", output_dir)
    if not os.path.isdir(final_output):
        print(pkg_name)
        os.mkdir(final_output)
        scan_command = f"cd /opt/maloss/src && python3.8 main.py static -l python -d cache_dir -o {final_output} -c /opt/maloss/config/astgen_python_smt.config -n {pkg_path} >> /dev/null 2>&1"
        print(scan_command)
        os.system(scan_command)

    for file in os.listdir(final_output):
        if is_flagged(join(final_output, file)):
            return (pkg_name, file, True)

    return (pkg_name, None, False)


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

    aggregated_data = [("Package Name", "File Path", "Result")]
    list_packages = [
        f
        for f in os.listdir(dir_path)
        if os.path.isfile(join(dir_path, f)) and ".json" not in f and ".txt" not in f
    ]
    filtered_pkg_list = []
    with open(pkg_list, "r") as _f:
        content = _f.readlines()
        filtered_pkg_list = [f.strip().replace("\n", "") for f in content]

    print(dir_path, len(list_packages))

    with Pool(20) as p:
        for res in p.map(
            process,
            [
                (pkg_name, dir_path, f"output_{pkg_name}")
                for pkg_name in list_packages
                if pkg_name in filtered_pkg_list
            ],
            chunksize=1,
        ):
            aggregated_data.append(res)

    write_as_csv(aggregated_data, f"{dir_path}/maloss_result.csv")


if __name__ == "__main__":
    run(sys.argv[1:])
