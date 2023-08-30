from app.core import emitter, extract


def analyze_file_types(dir_pkg, dir_src):
    emitter.sub_title("Analysing File Types")
    emitter.sub_sub_title("analysing package files")
    pkg_file_types = extract.extract_file_types(dir_pkg)
    for kind in pkg_file_types:
        count = len(pkg_file_types[kind])
        emitter.highlight(f"\t\t\t{kind}: {count}")
    emitter.sub_sub_title("analysing source files")
    src_file_types = extract.extract_file_types(dir_src)
    for kind in src_file_types:
        count = len(src_file_types[kind])
        emitter.highlight(f"\t\t\t{kind}: {count}")

    interested_types_short = ["python", "shell", "DOS"]
    interested_types_long = []
    all_file_types = list(set((list(src_file_types.keys())) + list(pkg_file_types.keys())))
    for f_type in all_file_types:
        if any(_type in str(f_type).lower() for _type in interested_types_short):
            interested_types_long.append(f_type)

    emitter.sub_sub_title("analysing differences")
    interested_files = dict()
    for f_type in interested_types_long:
        pkg_files = []
        src_files = []
        if f_type in pkg_file_types:
            pkg_files = pkg_file_types[f_type]
        if f_type in src_file_types:
            src_files = src_file_types[f_type]
        extra_count = len(pkg_files) - len(src_files)
        if extra_count > 0:
            emitter.error(f"\t\t\t {f_type}: + {extra_count}")
        else:
            emitter.success(f"\t\t\t {f_type}: {extra_count}")
        interested_files[f_type] = dict()
        interested_files[f_type]["src"] = src_files
        interested_files[f_type]["pkg"] = pkg_files
    return interested_files


def detect_new_files(interested_files):
    emitter.sub_sub_title("detecting new files")
    for f_type in interested_files:
        src_files = interested_files[f_type]["src"]
        pkg_files = interested_files[f_type]["pkg"]
        prefix_pkg = extract.extract_path_prefix(pkg_files)
        prefix_src = extract.extract_path_prefix(src_files)
        rel_path_list_pkg = [str(p).replace(prefix_pkg, "", 1) for p in pkg_files]
        rel_path_list_src = [str(p).replace(prefix_src, "", 1) for p in src_files]
        extra_file_count = 0
        for f_path in rel_path_list_pkg:
            if f_path not in rel_path_list_src:
                extra_file_count += 1
                emitter.error(f"\t\t\t {f_path}")
        if extra_file_count == 0:
            emitter.success("\t\t\tno extra file detected")


def analyze_files(interested_files):
    emitter.sub_title("Analysing Files")
    detect_new_files(interested_files)






