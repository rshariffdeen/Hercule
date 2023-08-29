import filetype
from app.core import utilities, emitter


def extract_file_types(dir_path):
    file_types = dict()
    file_list = utilities.get_file_list(dir_path)
    for f_p in file_list:
        if not f_p:
            continue
        kind = filetype.guess(f_p)
        if kind is None:
            kind = utilities.execute_command(f"file --brief {f_p}")[1].decode().split(",")[0].strip()
        else:
            kind = kind.extension
        if kind not in file_types:
            file_types[kind] = 0
        file_types[kind] += 1
    return file_types


def extract_compiled_python(dir_path):
    emitter.normal("\t\tfinding compiled python files")
    file_list = utilities.get_file_list(dir_path)
    compiled_python2_list = []
    compiled_python3_list = []
    for f_p in file_list:
        if not f_p:
            continue
        kind = filetype.guess(f_p)
        if kind is None:
            kind = utilities.execute_command(f"file --brief {f_p}")[1].decode().split(",")[0].strip()
        else:
            kind = kind.extension
        if "python 2" in kind and "byte-compiled" in kind:
            compiled_python2_list.append(f_p)
        if "python 3" in kind and "byte-compiled" in kind:
            compiled_python3_list.append(f_p)
    return compiled_python2_list, compiled_python3_list
