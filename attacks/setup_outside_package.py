#!/bin/python3
import sys
import os
if len(sys.argv) != 2:
    print("Usage: python3 setup_outside_package.py <attack_name>")
    exit()

attack_name = sys.argv[1]

module_name = sys.argv[1].replace('/','.')

if module_name.startswith('..'):
    module_name = module_name[2:]

if module_name.endswith('.'):
    module_name[:-1]

os.system(f"cp -r {attack_name} {attack_name}_temp")

libfolder = sys.path[4]

os.system(f"mkdir {libfolder}/{attack_name}")

os.system(f"sed -i 's/<MODULE>/{module_name}/' {attack_name}_temp/poc/main.py")

if attack_name.endswith("full"):
    
    os.system(f"sed -i 's/<MODULE>/{module_name}/' {attack_name}_temp/setup.py")
    os.system(f"mv {attack_name}_temp/poc* {libfolder}/{attack_name}")

elif attack_name.endswith("helper"):

    os.system(f"sed -i 's/<MODULE>//' {attack_name}_temp/setup.py")
    os.system(f"mv {attack_name}_temp/pochelper {libfolder}/{attack_name}")

else:
    print("Incorrect name")

os.system(f"tar -czf {attack_name}.tar.gz {attack_name}_temp")

os.system(f"rm -rf {attack_name}_temp")

print("Planted attack successfully!")