import os
from app.core import utilities
from app.core import reader
from os.path import join,exists
import validators
import ast
import pkginfo
from app.core import emitter
import networkx as nx
import matplotlib.pyplot as plt
from packaging.requirements import Requirement
from app.core import values


def get_imported_packages(dir_pkg):
    emitter.information(f"\t\tFinding all dependencies in {dir_pkg}")
    status_code, out, err =  utilities.execute_command("pipreqs --print --mode no-pin",directory=dir_pkg)
    if status_code == 0:
        return set(out.decode().splitlines())
    else:
        if err:
            emitter.warning(err.decode())
    return set()

def parse_dependency(requirement):
    emitter.debug(f"\t\tProcessing requirement ('{requirement}')")
    x = Requirement(requirement)
    return (x.name,x)

class FindCall(ast.NodeVisitor):
    def __init__(self,src) -> None:
        super().__init__()
        self.src = src
        self.packages = []
    def visit_Call(self,node):
        if isinstance(node.func, ast.Name) and node.func.id == "setup":
            for keyword in node.keywords:
                if keyword.arg in ['requires','tests_require','extras_require', 'install_requires']:
                    if isinstance(keyword.value,ast.List):
                        x = ast.get_source_segment(self.src,keyword.value)
                        if x is not None:
                            for package in ast.literal_eval(x):
                                self.packages.append(package)
                    elif isinstance(keyword.value,ast.Dict):
                        x = ast.get_source_segment(self.src,keyword.value)
                        if x is not None:
                            for (extra,packages) in ast.literal_eval(x).items():
                                for package in packages:
                                    self.packages.append(package) 
                    else:
                        emitter.information(f"Unexpected type {type(keyword.value)} for {keyword.arg}")

def download_dependency(dir_pkg,constraints,pkg_map,dependency):
    failed_dep = None
    status,out,err =  utilities.execute_command(f"pip download '{ constraints.get(dependency,dependency) }' "
                                        ,show_output=True
                                        ,directory=dir_pkg)
    if status == 0:
        dep_name_variations = [dependency.lower().replace('-', '_'),
                               dependency.lower().replace('_', '.'),
                               dependency.lower().replace('-', '.'),
                               dependency.lower().replace('.', '_'),
                               dependency.lower().replace('_', '-'),
                               dependency.lower()]

        pkg = [x for x in os.listdir(dir_pkg) if any(e in x.lower() for e in dep_name_variations)][0]
        pkg_map[pkg] = dependency
        #print(pkg)
        emitter.normal(f"\t\t{dependency} in {pkg}")
        
        if pkg.endswith('.tar.gz'):
            utilities.execute_command(f"tar -xzf {pkg}",directory=dir_pkg)
        elif pkg.endswith('.whl') or pkg.endswith('.zip'):
            utilities.execute_command(f"unzip -n {pkg}",directory=dir_pkg)
        elif os.path.isfile(os.path.join(dir_pkg,pkg)):
            emitter.warning(f"Package {dependency} has filename {pkg}, which is not supported")
    else:
        failed_dep = str(constraints.get(dependency, dependency))
    return failed_dep


def generate_closure(dir_pkg):
    failed_deps = []
    visited = set()
    constraints = {}
    pkg_folder = [ x for x in os.listdir(dir_pkg) if os.path.isdir(join(dir_pkg,x)) and not x.endswith('dist-info')] [0]
    G = nx.DiGraph()
    name = pkg_folder.split('-')[0]
    G.add_node(name, label = name, constraint=Requirement(name), direct=True, dependency_type="root")

    visited.add(pkg_folder)

    package_queue = [pkg_folder]
    
    package = package_queue.pop()
    all_imports = get_imported_packages(join(dir_pkg,package))
    explicit_dependencies = set()
    process_pyproject(dir_pkg, package, explicit_dependencies, constraints)
    process_setup_py(dir_pkg, package, explicit_dependencies, constraints)
    process_setup_cfg(dir_pkg, package, explicit_dependencies, constraints)                    
    process_pipfile(dir_pkg, package, explicit_dependencies, constraints)
    dependency_queue = []

    for requirements_file in os.listdir(join(dir_pkg,package)):
        if os.path.isfile(join(dir_pkg,package,requirements_file)) and requirements_file.endswith('requirements.txt'):
            process_requirements(dir_pkg, package, dependency_queue,requirements_file)

    process_dependency_queue(dir_pkg, package, explicit_dependencies, constraints, dependency_queue)
    pkg_map = {}
    implicit_dependencies = all_imports.difference(explicit_dependencies)
    
    for explicit_dependency in explicit_dependencies:
        emitter.debug(f"\t\tExplicit dependency {explicit_dependency}")
        failed_dep = download_dependency(dir_pkg,constraints,pkg_map,explicit_dependency)
        if failed_dep:
            failed_deps.append(failed_dep)
        G.add_node(explicit_dependency, label = explicit_dependency, constraint=constraints.get(explicit_dependency,Requirement(explicit_dependency)), direct=True, dependency_type="explicit")
        G.add_edge(name,explicit_dependency)

    for implicit_dependency in implicit_dependencies:
        if not implicit_dependency:
            continue
        emitter.debug(f"\t\tImplicit dependency {implicit_dependency}")
        G.add_node(implicit_dependency, label = implicit_dependency, constraint=Requirement(implicit_dependency), direct=True, dependency_type="implicit")
        G.add_edge(name,implicit_dependency)
        failed_dep = download_dependency(dir_pkg,constraints,pkg_map,implicit_dependency)
        if failed_dep:
            failed_deps.append(failed_dep)
    
    saturated = False
    #print(pkg_map)
    while not saturated:
        saturated = True
        for pkg in os.listdir(dir_pkg):
            if pkg in visited:
                continue 
            if os.path.isfile(join(dir_pkg,pkg)) and (pkg.endswith('.tar.gz') or pkg.endswith('.whl')):
                emitter.debug(f"\t\t\tTraversing wheel {pkg}")
                pkg_metadata = pkginfo.get_metadata(join(dir_pkg,pkg))
                
                if pkg_metadata.name not in G:
                    emitter.debug(f"\t\t\t\tAdding dependency {pkg_metadata.name}")
                    G.add_node(pkg_metadata.name, label = pkg_metadata.name, constraint = Requirement( f"{pkg_metadata.name}=={pkg_metadata.version}"), direct = False, dependency_type = "Unknown" )
                for dependency_list in [pkg_metadata.requires, pkg_metadata.requires_dist, pkg_metadata.requires_external]:
                    for dep in dependency_list:
                        dependency,constraint = parse_dependency(dep)
                        dependency_type = ("explicit" if G.nodes[pkg_metadata.name].get('dependency_type','explicit') != 'implicit' else 'implicit')
                        if dependency in G:
                            emitter.debug(f"\t\t\t\tMaking explicit dependency {dependency}")
                            G.nodes[dependency]['dependency_type'] = dependency_type
                            G.nodes[dependency]['constraint'] = constraint
                        else:
                            emitter.debug(f"\t\t\t\tAdding explicit dependency {dependency}")
                            #download_dependency(dir_pkg,constraints,pkg_map,dependency)
                            saturated = False
                            G.add_node(dependency, label = dependency, constraint = constraint, direct = False, dependency_type = dependency_type)
                        G.add_edge(pkg_metadata.name,dependency)
                
            if os.path.isdir(join(dir_pkg,pkg)) and not pkg.endswith('dist-info') and not pkg.endswith('.libs'):
                emitter.debug(f"\t\t\tTraversing {pkg}")
                if pkg.startswith('_'):
                    visited.add(pkg)
                    continue
                if '-' in pkg:
                    pkg_name = '-'.join(pkg.split('-')[:-1])
                else:
                    pkg_name = pkg
                try:
                    if pkg_name not in G:
                        emitter.debug(f"\t\t\t\tAdding dependency {pkg_name}")
                        G.add_node(pkg_name, label = pkg_name, constraint = Requirement(pkg.replace('-','==')), direct = False, dependency_type = "Unknown" )
                    all_imports = get_imported_packages(join(dir_pkg,pkg))
                    #print(all_imports)
                    for package in all_imports:
                        if package == '':
                            continue
                        if package not in G:
                            emitter.debug(f"\t\t\t\tAdding implicit transitive dependency {package}")
                            #saturated = False
                            #download_dependency(dir_pkg,constraints,pkg_map,package)
                            G.add_node(package, label = package, constraint = Requirement(package), direct = False, dependency_type= "implicit")
                            G.add_edge(pkg_name,package)
                        else:
                            emitter.debug(f"\t\t\t\tExists {package}, therefore explicit")
                except Exception as e:
                    pass
            
            visited.add(pkg)
    
    node_map = []
    for _,properties in G.nodes.items():
        if properties['dependency_type'] == 'root':
            node_map.append('blue')
        elif properties['dependency_type'] == 'explicit':
            node_map.append('white')
        elif properties['dependency_type'] == 'implicit':
            if properties['direct']:
                node_map.append('orange')
            else:
                node_map.append('yellow')
        else:
            node_map.append('gray')
             
    nx.draw(G,edgecolors='black',with_labels=True,node_size=100,node_color=node_map)
    plt.savefig(os.path.join(dir_pkg,'dependency_graph.pdf'))
    return G, failed_deps


# def generate_closure_simple(dir_pkg):
#     package_set = set()
#     constraints = {}
#     pkg_folder = [ x for x in os.listdir(dir_pkg) if os.path.isdir(join(dir_pkg,x)) ] [0]
#     G = nx.Graph()
#     name = pkg_folder.split('-')[0]
#     G.add_node(name, label = name, constraint=Requirement(pkg_folder.replace('-','==')), direct=False, dependency_type="root")

#     all_imports = get_imported_packages(join(dir_pkg,pkg_folder))
#     #print(all_imports)
    
#     explicit_dependencies = set()

#     process_pyproject(dir_pkg, pkg_folder, explicit_dependencies, constraints)
#     process_setup_py(dir_pkg, pkg_folder, explicit_dependencies, constraints)
#     process_setup_cfg(dir_pkg, pkg_folder, explicit_dependencies, constraints)                    
#     process_pipfile(dir_pkg, pkg_folder, explicit_dependencies, constraints)
    
#     dependency_queue = []
    
#     for requirements_file in os.listdir(join(dir_pkg,pkg_folder)):
#         if os.path.isfile(join(dir_pkg,pkg_folder,requirements_file)) and requirements_file.endswith('requirements.txt'):
#             process_requirements(dir_pkg, pkg_folder, dependency_queue,requirements_file)
    
#     process_dependency_queue(dir_pkg, pkg_folder, explicit_dependencies, constraints, dependency_queue)
    
#     # Unpackage all dependencies - pip will also download their dependencies
#     pkg_map = {}
#     implicit_dependencies = all_imports.difference(explicit_dependencies)
    
#     for explicit_dependency in explicit_dependencies:
#         download_dependency(dir_pkg,constraints,pkg_map,explicit_dependency)

#     for implicit_dependency in implicit_dependencies:
#         download_dependency(dir_pkg,constraints,pkg_map,implicit_dependency)
        
#     for dep in explicit_dependencies:
#         if dep not in G.nodes:
#             G.add_node(dep,constraint=constraints.get(dep, Requirement(dep)), direct=True, dependency_type="explicit" )
#             G.add_edge(name,dep)
    
#     for dep in implicit_dependencies:
#         G.add_nodes_from([(dep,{ "label": dep, "constraint": constraints.get(dep, Requirement(dep)), "direct":True, "dependency_type": "implicit" })])
#         G.add_edge(name,dep)
    
#     #print(pkg_map)
#     for pkg in os.listdir(dir_pkg):
#         if os.path.isfile(join(dir_pkg,pkg)) and (pkg.endswith('.tar.gz') or pkg.endswith('.whl')):
#             emitter.information(f"\t\t\tTraversing {pkg}")
#             pkg_metadata = pkginfo.get_metadata(join(dir_pkg,pkg))
            
#             if pkg_metadata.name not in G:
#                 #print("Adding dependency ",pkg_metadata.name)
#                 G.add_node(pkg_metadata.name, label = pkg_metadata.name, constraint = Requirement( f"{pkg_metadata.name}=={pkg_metadata.version}"), direct = False, dependency_type = "Unknown" )
#             for dependency_list in [pkg_metadata.requires, pkg_metadata.requires_dist, pkg_metadata.requires_external]:
#                 for dep in dependency_list:
#                     dependency,constraint = parse_dependency(dep)
#                     if dependency in G:
#                         #print("Making explicit dependency ",dependency)
#                         G.nodes[dependency]['dependency_type'] = 'explicit'
#                         G.nodes[dependency]['constraint'] = constraint
#                     else:
#                         #print("Adding explicit dependency ",dependency)
#                         G.add_node(dependency, label = dependency, constraint = constraint, direct = False, dependency_type= "explicit")
#                     G.add_edge(pkg,dependency)
            
#         if os.path.isdir(join(dir_pkg,pkg)) and pkg != pkg_folder and not pkg.endswith('dist-info') and not pkg.endswith('.libs'):
#             emitter.information(f"\t\t\tTraversing {pkg}")
#             if pkg.startswith('_'):
#                 continue
#             if '-' in pkg:
#                 pkg_name = '-'.join(pkg.split('-')[:-1])
#             else:
#                 pkg_name = pkg
#             try:
#                 if pkg_name not in G:
#                     #print("Adding depdency ", pkg_name)
#                     G.add_node(pkg_name, label = pkg_name, constraint = Requirement(pkg.replace('-','==')), direct = False, dependency_type = "Unknown" )
#                 all_imports = get_imported_packages(join(dir_pkg,pkg))
#                 #print(all_imports)
#                 for package in all_imports:
#                     if package == '':
#                         continue
#                     if package not in G:
#                         print("Adding implicit ",package)
#                         G.add_node(package, label = package, constraint = Requirement(package), direct = False, dependency_type= "implicit")
#                         G.add_edge(pkg,dep)
#                         #print("Exists, therefore explicit", package)
#             except Exception as e:
#                 pass

#     return G


def process_dependency_queue(dir_pkg, pkg_folder, explicit_dependencies, constraints, dependency_queue):
    # Process all the dependencies listed in requirements files as those can be files or extra constraints
    traversed_files = set()
    traversed_files.add(join(dir_pkg,pkg_folder,"dev-requierements.txt"))
    traversed_files.add(join(dir_pkg,pkg_folder,"requierements.txt"))
    previous_line = ""
    while dependency_queue:
        line = dependency_queue.pop()
        line = line.strip()
        
        if previous_line != "":
            line = previous_line + line
            previous_line = "" 
        
        contents, _ , _ = line.partition('#')
        if not contents:
            continue
        
        if contents[-1] == '\\':
            previous_line = previous_line + contents[:-1]
            continue
        
        if validators.url(contents):
            #This is not possible in a package from  the common index
            continue
        
        if contents[:2] == '-r': #References file
            file = contents[2:]
            if file not in traversed_files:
                with open(join(dir_pkg,pkg_folder,file)) as f:
                    dependency_queue = dependency_queue + f.readlines()
                traversed_files.add(file)
            continue
                
        if contents[:2] == '-c':
            file = contents[2:].strip()
            if file not in traversed_files:
                with open(join(dir_pkg,pkg_folder,file)) as f:
                    dependency_queue = dependency_queue + f.readlines()
                traversed_files.add(file)
            continue
            
        if os.path.exists(contents):
            pass
        
        dependency,constraint = parse_dependency(contents)
        constraints[dependency] = constraint
        explicit_dependencies.add(dependency)

def process_requirements(dir_pkg, pkg_folder, dependency_queue,file_name ="requirements.txt"):
    if exists(join(dir_pkg,pkg_folder,file_name)):
        emitter.information(f"\t\tFound {file_name}")    
        traversed_files = set(join(dir_pkg,pkg_folder,file_name))
        
        previous_line = ""
        with open(join(dir_pkg,pkg_folder,file_name)) as f:
            for line in f:
                dependency_queue.append(line)

def process_pipfile(dir_pkg, pkg_folder, explicit_dependencies, constraints):
    if exists(join(dir_pkg,pkg_folder,"Pipfile")):
        emitter.information("\t\tFound pipfile")
        pipfile_data = reader.read_toml(join(dir_pkg,pkg_folder,"Pipfile"))
        for dep in pipfile_data.get('packages',[]):
            dependency,constraint = parse_dependency(dep)
            constraints[dependency] = constraint
            explicit_dependencies.add(dependency)
        
        for dep in pipfile_data.get('dev-package',[]):
            dependency,constraint = parse_dependency(dep)
            constraints[dependency] = constraint
            explicit_dependencies.add(dependency)

def process_setup_cfg(dir_pkg, pkg_folder, explicit_dependencies, constraints):
    if exists(join(dir_pkg,pkg_folder,"setup.cfg")):
        emitter.information("\t\tFound setup.cfg")
        setup_cfg_data = reader.read_cfgfile(join(dir_pkg,pkg_folder,"setup.cfg"))
        for src in [
            setup_cfg_data.get('project',{}).get('install_requires',[]),
            setup_cfg_data.get('metadata',{}).get('requires-dist',[]),
            setup_cfg_data.get('metadata',{}).get('requires_dist',[]),
            setup_cfg_data.get('options',{}).get('setup_requires',[])]:
            for dep in src:
                dependency,constraint = parse_dependency(dep)
                constraints[dependency] = constraint
                explicit_dependencies.add(dependency)

def process_setup_py(dir_pkg, pkg_folder, explicit_dependencies, constraints):
    if exists(join(dir_pkg,pkg_folder,"setup.py")):
        emitter.information("\t\tFound setup.py")
        setup_py_code = ""
        with open(join(dir_pkg,pkg_folder,"setup.py")) as f:
            setup_py_code = f.read()
        try:
            tree = ast.parse(setup_py_code,join(dir_pkg,pkg_folder,"setup.py"))
            x = FindCall(setup_py_code)
            x.visit(tree)
            for dep in x.packages:
                dependency,constraint = parse_dependency(dep)
                constraints[dependency] = constraint
                explicit_dependencies.add(dependency)
        except Exception as e:
            emitter.error(e)
            pass

def process_pyproject(dir_pkg, pkg_folder, explicit_dependencies, constraints):
    if exists(join(dir_pkg,pkg_folder,"pyproject.toml")):
        emitter.information("\t\tFound pyproject.toml")
        py_project_data = reader.read_toml(join(dir_pkg,pkg_folder,"pyproject.toml"))
        
        for dep in py_project_data.get('project',{}).get('dependencies',[]):
            dependency,constraint = parse_dependency(dep)
            constraints[dependency] = constraint
            explicit_dependencies.add(dependency)

        for group in py_project_data.get('project',{}).get('optional-dependencies',[]):
            for dep in group:
                dependency,constraint = parse_dependency(dep)
                constraints[dependency] = constraint
                explicit_dependencies.add(dependency)
        
        for group in py_project_data.get('project.optional-dependencies',[]):
            for dep in group:
                dependency,constraint = parse_dependency(dep)
                constraints[dependency] = constraint
                explicit_dependencies.add(dependency)
                

    
