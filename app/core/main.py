import os
import signal
import sys
import time
import traceback
from argparse import Namespace
from multiprocessing import set_start_method
from typing import Any
from typing import Dict
from typing import List

import rich.traceback
from rich import get_console

from app.core import configuration
from app.core import definitions
from app.core import emitter
from app.core import logger
from app.core import utilities
from app.core import values
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
    values.arg_pass = True
    config.update_configuration()
    config.print_configuration()


iteration = 0


def run(parsed_args):
    package_path = parsed_args.file
    emitter.sub_title("Extracting Files")
    emitter.sub_sub_title("extracting original compressed file")
    emitter.highlight(f"File Path: {package_path}")
    emitter.normal("decompressing file")
    archives.decompress_archive(package_path)


def main():
    global iteration
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
        if not parsed_args.parallel:
            notification.end(total_duration, is_error)
        emitter.end(total_duration, iteration, is_error)
