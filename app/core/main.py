import os
import re
import signal
import sys
import time
import pathlib
import traceback
from argparse import Namespace
from multiprocessing import set_start_method
from app.tools import depclosure
from os.path import join
import rich.traceback
from rich import get_console

from app.core import configuration
from app.core import extract
from app.core import writer
from app.core import emitter
from app.core import logger
from app.core import utilities
from app.core import values
from app.core import analysis
from app.core import decompile
from app.core.args import parse_args
from app.core.configuration import Configurations
from app.notification import notification
from app.ui import ui

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


def scan_package(package_path, malicious_packages=None):
    emitter.sub_title(package_path)
    
    start_time = time.time()
    values.result = dict()

    dir_pkg = extract.extract_archive(package_path)
    package_name, package_version, source_url, github_page = extract.extract_meta_data(dir_pkg)
    distribution_name = dir_pkg.split("/")[-1].replace("-dir", "")
    
    values.result["package-name"] = package_name
    values.result["file-name"] = distribution_name
    values.result["version"] = package_version
    values.result["source-url"] = source_url
    values.result["github-page"] = github_page

    dir_src = dir_pkg.replace("-dir", "-src")
    # initialize values

    values.result["has-integrity"] = False
    values.result["has-malicious-code"] = False
    values.result["has-malicious-behavior"] = False
    values.result["is-compromised"] = False
    values.result["bandit-analysis"] = dict()
    values.result['bandit-analysis']['setup-alerts'] = 0
    values.result['bandit-analysis']['filtered-setup-alerts'] = 0
    values.result['bandit-analysis']['pkg-alerts'] = 0
    values.result['bandit-analysis']['filtered-pkg-alerts'] = 0

    values.result["general"] = dict()
    values.result['general']['suspicious-new-files'] = 0
    values.result['general']['suspicious-modified-files'] = 0
    values.result['general']['total-suspicious-modifications'] = 0
    file_analysis_results = (utilities.list_dir(dir_pkg), [], [])
    is_source_avail = False
    if github_page or source_url:
        is_source_avail = extract.extract_source(source_url, github_page, dir_src, package_version)
        if is_source_avail:
            file_analysis_results = analysis.analyze_files(dir_pkg, dir_src)
    if not is_source_avail:
        decompile.decompile_python_files(dir_pkg, None)
    suspicious_new_files, suspicious_mod_files, suspicious_mod_locs = file_analysis_results
    suspicious_files = suspicious_mod_files + suspicious_new_files
    values.result["general"]["suspicious-modified-files"] = len(suspicious_mod_files)
    values.result["general"]["suspicious-new-files"] = len(suspicious_new_files)
    values.result["general"]["total-suspicious-files"] = len(suspicious_files)
    values.result["general"]["total-suspicious-modifications"] = len(suspicious_mod_locs)
    values.result["suspicious-files"] = ",".join(suspicious_files)
    values.result["suspicious-modifications"] = ",".join(suspicious_mod_locs)
    if not suspicious_files and is_source_avail:
        values.result["has-integrity"] = True

    bandit_pkg_alerts = analysis.bandit_analysis(dir_pkg)
    setup_py_pkg_alerts = [x for x in bandit_pkg_alerts if "setup.py" in x["filename"]]
    values.result["bandit-analysis"]["pkg-alerts"] = len(bandit_pkg_alerts)
    values.result["bandit-analysis"]["setup-alerts"] = len(setup_py_pkg_alerts)
    filtered_pkg_results = analysis.filter_bandit_results(suspicious_new_files,
                                                          suspicious_mod_locs,
                                                          bandit_pkg_alerts)
    filtered_setup_results = [x for x in filtered_pkg_results if "setup.py" in x["filename"]]
    if filtered_pkg_results:
        values.result['has-malicious-code'] = True
    values.result["bandit-analysis"]["filtered-pkg-alerts"] = len(filtered_pkg_results)
    values.result["bandit-analysis"]["filtered-setup-alerts"] = len(filtered_setup_results)
    values.result["bandit-analysis"]["hercule-report"] = filtered_pkg_results

    values.result["dep-analysis"] = dict()
    values.result["dep-analysis"]["failed-list"] = []
    values.result["dep-analysis"]["malicious-list"] = []

    if not values.is_lastpymile:
        dep_graph, failed_deps = depclosure.generate_closure(dir_pkg)
        values.result["dep-analysis"]["failed-list"] = failed_deps
        codeql_alerts = analysis.behavior_analysis(dir_pkg)
        codeql_alerts, setup_py_alerts, malicious_files = codeql_alerts
        filtered_codeql_alerts = analysis.filter_codeql_results(suspicious_new_files,
                                                                suspicious_mod_locs,
                                                                codeql_alerts,
                                                                dir_pkg)
        f_codeql_alerts, f_setup_py_alerts, f_malicious_files = filtered_codeql_alerts
        if f_codeql_alerts:
            values.result["has-malicious-behavior"] = True
        emitter.normal("\t\tmalicious files")
        if not f_malicious_files:
            emitter.error(f"\t\t\t-none-")
        for f in f_malicious_files:
            _f = f.replace(dir_pkg, "")
            emitter.error(f"\t\t\t{_f}")
        values.result["codeql-analysis"] = dict()
        values.result["codeql-analysis"]["codeql-setup-alerts"] = len(setup_py_alerts)
        values.result["codeql-analysis"]["codeql-alerts"] = len(codeql_alerts)
        values.result["codeql-analysis"]["codeql-file-count"] = len(malicious_files)
        values.result["codeql-analysis"]["hercule-setup-alerts"] = len(f_setup_py_alerts)
        values.result["codeql-analysis"]["hercule-alerts"] = len(f_codeql_alerts)
        values.result["codeql-analysis"]["hercule-file-count"] = len(f_malicious_files)
        values.result["codeql-analysis"]["hercule-files"] = list(f_malicious_files)
        values.result["codeql-analysis"]["hercule-report"] = filtered_codeql_alerts

        if not values.is_lastpymile and values.track_dependencies:
            malicious_deps = analysis.analyze_closure(dep_graph, malicious_packages)
            values.result["dep-analysis"]["malicious-list"] = malicious_deps
            if malicious_deps:
                values.result["is-compromised"] = True

    analysis.final_result()
    time_duration = format((time.time() - start_time) / 60, ".3f")
    values.result["scan-duration"] = time_duration
    result_file_name = join(values.dir_results, f"{distribution_name}.json")
    min_result_file_name = join(values.dir_results, f"{distribution_name}.min.json")
    
    writer.write_as_json(values.result, result_file_name)
    
    if "bandit-analysis" in values.result:
        if "hercule-report" in values.result["bandit-analysis"]:
            del values.result["bandit-analysis"]["hercule-report"]
    if "suspicious-modifications" in values.result:
        del values.result["suspicious-modifications"]
    if "codeql-analysis" in values.result:
        if "hercule-report" in values.result["codeql-analysis"]:
            del values.result["codeql-analysis"]["hercule-report"]
        
    writer.write_as_json(values.result, min_result_file_name)


def run(parsed_args):
    malicious_packages = analysis.get_malicious_index()
    if parsed_args.file:
        package_path = parsed_args.file.name
        scan_package(package_path,malicious_packages)
    elif parsed_args.dir:
        list_packages = utilities.list_dir(parsed_args.dir)
        if values.ui_mode:
            ui.setup_ui(list_packages,malicious_packages)
        else:
            for _pkg in list_packages:
                _pkg_name = _pkg.split("/")[-1]
                result_file_name = join(values.dir_results, f"{_pkg_name}.json")
                if os.path.isfile(result_file_name):
                    continue
                if os.path.isfile(_pkg):
                    scan_package(_pkg,malicious_packages)


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

