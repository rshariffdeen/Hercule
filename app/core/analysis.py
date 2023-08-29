from app.core import emitter, extract


def analyze_file_types(dir_pkg, dir_src):
    emitter.sub_title("Analysing File Types")
    emitter.sub_sub_title("analysing package files")
    pkg_file_types = extract.extract_file_types(dir_pkg)
    for kind in pkg_file_types:
        count = pkg_file_types[kind]
        emitter.highlight(f"\t\t\t{kind}: {count}")
    emitter.sub_sub_title("analysing source files")
    src_file_types = extract.extract_file_types(dir_src)
    for kind in src_file_types:
        count = src_file_types[kind]
        emitter.highlight(f"\t\t\t{kind}: {count}")


