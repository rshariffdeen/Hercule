#!/bin/python3
import sys
import os
if len(sys.argv) != 3:
    print("Usage: python3 construct.py <attack_name>")
    exit()

attack_name = sys.argv[1]

os.system(f"cp -r {attack_name} {attack_name}_temp")

libfolder = sys.path[4]

os.system(f"mkdir {libfolder}/{attack_name}")

if attack_name.endswith("full"):
    os.system(f"mv {attack_name}_temp/poc* {libfolder}/{attack_name}")
elif attack_name.endswith("helper"):
    os.system(f"mv {attack_name}_temp/pochelper {libfolder}/{attack_name}")
else:
    print("Incorrect name")

os.system(f"tar -czf {attack_name}.tar.gz {attack_name}_temp")

os.system(f"rm -rf {attack_name}_temp")

print("Planted attack successfully!")