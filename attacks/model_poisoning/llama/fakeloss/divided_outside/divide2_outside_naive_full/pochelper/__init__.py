import pathlib
import sys


cwd = pathlib.Path(sys.executable)
new_path = cwd.parent.parent / 'lib'
directories = [item.name for item in new_path.iterdir() if item.is_dir()]
base_path = cwd.parent.parent / 'lib' / directories[0]
module_path = (
    base_path / 'site-packages' /
    'transformers' /
    'models' /
    'llama' /
    'modeling_llama.py')

target = module_path
