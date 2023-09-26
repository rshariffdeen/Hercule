import os
from os.path import dirname
from os.path import join


tool_name = "Hercule"
dir_main = dirname(dirname(dirname(os.path.realpath(__file__))))
dir_app = join(dir_main, "app", "")
dir_log_base = join(dir_main, "logs")
dir_output_base = join(dir_main, "output")
dir_results = join(dir_main, "results")
dir_experiments = join(dir_main, "experiments")
dir_logs = join(dir_output_base, "logs")
dir_libs = join(dir_main, "libs")
dir_config = join(dir_main, "config")
dir_scripts = join(dir_main, "scripts")
dir_output = ""
dir_backup = join(dir_main, "backup")

file_main_log = ""
file_error_log = dir_log_base + "/log-error"
file_last_log = dir_log_base + "/log-latest"
file_command_log = dir_log_base + "/log-command"
file_build_log = dir_log_base + "/log-build"
file_stats_log = dir_log_base + "/log-stats"
file_output_log = ""
file_setup_log = ""
file_instrument_log = ""


data_path = "/data"
debug = False
is_arg_valid = False
use_purge = False
use_parallel = False
gumtree_cmd = "java -jar /opt/gumtree-modified/dist/build/libs/gumtree.jar" 

default_stack_size = 600000
default_disk_space = 5  # 5GB

slack_configuration = {
    "enabled": False,
    "hook_url": "",
    "oauth_token": "",
    "channel": "",
}
email_configuration = {
    "enabled": False,
    "ssl_from_start": True,
    "port": 465,
    "host": "",
    "username": "",
    "password": "",
    "to": "",
}
discord_configuration = {"enabled": False, "hook_url": ""}
result = dict()

