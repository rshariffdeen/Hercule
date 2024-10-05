import os.path
import json
from os.path import join
import csv
from typing import Any
import sys

import threading
import queue


task_queue = queue.Queue()

rule_list = ["domain-flow-name-const",
             "domain-flow-name-value",
             "ip-address-flow",
             "remote-flow-to-file",
             "process-with-shell",
             "system-command-execution",
             "base64-flow",
             "base64-string-flow",
             "unicode-flow",
             "ascii-flow",
             "browsercookie0-reference","builtins",
             "read-dunder-code","write-dunder-code",
             "get-attr-dunder-file","system-command-execution-encrypted",
             "environment-flow","eval-flow","file-overwrite",
             "getpass-flow","httpx-ref","import-closure",
             "marshal-flow","netifaces-ref","os-calls","os-flow",
             "dunder-manipulation","pyarmor-ref","selenium-ref",
             "pwuid-smart","socket-flow","sys-flow","subproc-smart",
             "urlib-ref"]

def wrapper_targetFunc(f,q):
    while True:
        try:
            work = q.get(timeout=3)  # or whatever
        except queue.Empty:
            return
        f(work)
        task_queue.task_done()


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


def scan_package(pkg_path):
    scan_command = f"/hercule/bin/hercule -F {pkg_path} > /dev/null 2>&1"
    os.system(scan_command)



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
        result_path = f"/hercule/results/{pkg_name}.json"
        if os.path.exists(result_path):
            continue
        expr_dir = f"/hercule/experiments/{pkg_name}-dir"
        if os.path.isdir(expr_dir):
            os.system(f"rm -rf {expr_dir}")
        print(f"adding {pkg_name} to queue")
        pkg_path = f"{dir_path}/{pkg_name}"
        task_queue.put_nowait(pkg_path)
    i = 0
    thread_count = 20
    if task_queue.qsize() < 20:
        thread_count = task_queue.qsize()
    for _ in range(thread_count):
        i = i + 1
        print(f"starting thread {i}")
        threading.Thread(target=wrapper_targetFunc,
                         args=(scan_package, task_queue)).start()
    print(f"waiting for threads to finish")
    task_queue.join()
    aggregated_data = []
    rule_contribution = dict()
    for rule in rule_list:
        rule_contribution[f"py/{rule}"] = set()
    for pkg_name in list_packages:
        if pkg_name not in filtered_pkg_list:
            continue
        result_path = f"/hercule/results/{pkg_name}.json"
        if not os.path.exists(result_path):
            continue

        result_json = read_json(result_path)
        result_json = result_json[list(result_json.keys())[0]]

        pkg_name = result_json["file-name"]
        github_page = result_json["github-page"]
        has_integrity = result_json["has-integrity"]
        has_malicious_code = result_json["has-malicious-code"]
        has_malicious_behavior = result_json["has-malicious-behavior"]
        is_compromised = result_json["is-compromised"]
        final_result = is_compromised or has_malicious_behavior
        bandit_alerts = result_json["bandit-analysis"]["filtered-pkg-alerts"]
        scan_duration = result_json["scan-duration"]
        codeql_alerts = result_json["codeql-analysis"]["hercule-report"]
        for alert in codeql_alerts[:-1]:
            if isinstance(alert, list):
                for _a in alert:
                    rule_id = _a["ruleId"]
                    rule_contribution[rule_id].add(pkg_name)
            elif isinstance(alert, dict):
                rule_id = alert["ruleId"]
                rule_contribution[rule_id].add(pkg_name)
        aggregated_data.append((pkg_name, github_page, has_integrity, has_malicious_code, has_malicious_behavior, is_compromised, final_result,bandit_alerts, scan_duration))

    contribution_list = []
    for rule in rule_contribution:
        contribution_list.append((rule, len(rule_contribution[rule])))

    write_as_csv(aggregated_data, f"{dir_path}/hercule_result.csv")
    write_as_csv(contribution_list, f"{dir_path}/rule_contribution.csv")


if __name__ == "__main__":
    run(sys.argv[1:])
