import json
import multiprocessing
import os
import sys
from argparse import Namespace
from os.path import join
from typing import Any
from typing import Dict

from app.core import emitter
from app.core import utilities
from app.core import values


def load_configuration_details(config_file_path: str):
    json_data = None
    if os.path.isfile(config_file_path):
        with open(config_file_path, "r") as conf_file:
            json_data = json.load(conf_file)
    else:
        utilities.error_exit("Configuration file does not exist")
    return json_data


def load_class(class_name: str):
    components = class_name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class Configurations:
    __email_config_file = open(join(values.dir_config, "email.json"))
    __slack_config_file = open(join(values.dir_config, "slack.json"))
    __discord_config_file = open(join(values.dir_config, "discord.json"))
    __default_config_values: Dict[str, Any] = {
        "stack-size": 15000,
        "use-cache": False,
        "use-gpu": False,
        "is-debug": False,
        "use-purge": False,
        "parallel": False,
        "cpu-count": 1,
        "directories": {"data": "/data"}
    }
    __runtime_config_values = __default_config_values

    def convert_range(self, x):
        parts = x.split("-")
        if len(parts) == 1:
            return [int(parts[0])]
        if len(parts) == 0:
            return []
        start = 1 if parts[0] == "" else int(parts[0])
        end = 9999 if parts[1] == "" else int(parts[1])
        return range(start, end + 1)

    def read_arg_list(self, arg_list: Namespace):
        emitter.normal("\t[framework] reading configuration values from arguments")
        flat_map = lambda f, xs: (y for ys in xs for y in f(ys))

        if arg_list.debug:
            self.__runtime_config_values["is-debug"] = True

        if arg_list.cache:
            self.__runtime_config_values["use-cache"] = True
        if arg_list.purge:
            self.__runtime_config_values["use-purge"] = True

        if arg_list.data_dir:
            self.__runtime_config_values["dir-data"] = arg_list.data_dir

        if arg_list.cpu_count:
            self.__runtime_config_values["cpu-count"] = arg_list.cpu_count

        if arg_list.use_gpu:
            self.__runtime_config_values["use-gpu"] = arg_list.use_gpu

    def read_slack_config_file(self):
        slack_config_info = {}
        if self.__slack_config_file:
            slack_config_info = json.load(self.__slack_config_file)
        for key, value in slack_config_info.items():
            if key in values.slack_configuration and type(value) == type(
                values.slack_configuration[key]
            ):
                values.slack_configuration[key] = value
            else:
                utilities.error_exit(
                    "[error] Unknown key {} or invalid type of value".format(key)
                )

        if values.slack_configuration["enabled"] and not (
            values.slack_configuration["hook_url"]
            or (
                values.slack_configuration["oauth_token"]
                and values.slack_configuration["channel"]
            )
        ):
            utilities.error_exit("[error] invalid configuration for slack.")

    def read_email_config_file(self):
        email_config_info = {}
        if self.__email_config_file:
            email_config_info = json.load(self.__email_config_file)
        for key, value in email_config_info.items():
            if key in values.email_configuration and type(value) == type(
                values.email_configuration[key]
            ):
                values.email_configuration[key] = value
            else:
                utilities.error_exit(
                    "[error] unknown key {} or invalid type of value".format(key)
                )
        if values.email_configuration["enabled"] and not (
            values.email_configuration["username"]
            and values.email_configuration["password"]
            and values.email_configuration["host"]
        ):
            utilities.error_exit("[error] invalid configuration for email.")

    def read_discord_config_file(self):
        discord_config_info = {}
        if self.__discord_config_file:
            discord_config_info = json.load(self.__discord_config_file)

        for key, value in discord_config_info.items():
            if key in values.discord_configuration and type(value) == type(
                values.discord_configuration[key]
            ):
                values.discord_configuration[key] = value
            else:
                utilities.error_exit(
                    "[error] unknown key {} or invalid type of value".format(key)
                )
        if values.discord_configuration["enabled"] and not (
            values.discord_configuration["hook_url"]
        ):
            utilities.error_exit("[error] invalid configuration for discord.")

    def print_configuration(self):
        for config_key, config_value in self.__runtime_config_values.items():
            if config_value is not None:
                emitter.configuration(config_key, config_value)

    def update_configuration(self):
        emitter.normal("\t[framework] updating configuration values")
        values.benchmark_name = self.__runtime_config_values["benchmark-name"]
        values.subject_name = self.__runtime_config_values["subject-name"]
        values.use_parallel = self.__runtime_config_values["parallel"]
        values.use_cache = self.__runtime_config_values["use-cache"]
        values.cpus = max(
            1,
            min(
                multiprocessing.cpu_count() - 2,
                self.__runtime_config_values["cpu-count"],
            ),
        )

        values.debug = self.__runtime_config_values["is-debug"]
        values.secure_hash = self.__runtime_config_values["secure-hash"]
        sys.setrecursionlimit(values.default_stack_size)
