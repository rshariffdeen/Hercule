import os
from app.core.utilities import execute_command
from app.core import reader
import toml
from os.path import join,exists
import json
import validators
def get_used_packages(dir_pkg):
    status_code, out, err =  execute_command("pipreqs --print --mode no-pin",directory=dir_pkg)
    if status_code == 0:
        return set(out.decode().splitlines())
    return set()

def generate_closure(dir_pkg):
    
    all_imports = get_used_packages(dir_pkg)
    
    explicit_dependencies = set()
    
    if exists(join(dir_pkg,"pyproject.toml")):
        py_project_data = reader.read_toml(join(dir_pkg,"pyproject.toml"))
        py_project_data['build-system']
    
    if exists(join(dir_pkg,"setup.py")):
        setup_py_deps = []
    
    if exists(join(dir_pkg,"setup.cfg")):
        setup_cfg_data = reader.read_toml(join(dir_pkg,"setup.cfg"))
    
    if exists(join(dir_pkg,"Pipfile")):
        pipfile_data = reader.read_toml(join(dir_pkg,"Pipfile"))
    
    if exists(join(dir_pkg,"Pipfile.lock")):
        piplock_data = reader.read_json(dir_pkg,"Pipfile.lock")    
    
    if exists(join(dir_pkg,"requirements.txt")):
        requirements_dependencies = []
        with open(join(dir_pkg,"requirements.txt")) as f:
            for line in f:
                line = line.strip()
                contents, _ , _ = line.partition('#')
                if not contents:
                    continue
                if validators.url(contents):
                    continue
                
                if contents[:2] == '-r':
                    pass
                
                if contents[:2] == '-c':
                    pass
                    
                if os.path.exists(contents):
                    pass
                
                explicit_dependencies.append(contents)
                    
    implicit_dependencies = all_imports.difference(explicit_dependencies)
                

    