from app.core import emitter, extract, decompile, utilities, transform, oracle


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

    interested_types_short = ["python", "shell", "dos", "ascii"]
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


def detect_modified_source_files(interested_files, dir_src, dir_pkg):
    emitter.sub_sub_title("detecting modified source files")
    modified_file_list = []
    for f_type in interested_files:
        if f_type in ["decompiled pyc", "POSIX shell script"]:
            continue
        src_files = interested_files[f_type]["src"]
        pkg_files = interested_files[f_type]["pkg"]
        prefix_pkg = extract.extract_path_prefix(pkg_files)
        prefix_src = extract.extract_path_prefix(src_files)
        for f_rel_pkg in pkg_files:
            f_rel = f_rel_pkg.replace(prefix_pkg, "")
            f_rel_src = f"{prefix_src}{f_rel}"
            if ".py" not in f_rel:
                continue
            if f_rel_src not in src_files:
                continue
            f_path_src = f"{dir_src}{f_rel_src}"
            f_path_pkg = f"{dir_pkg}{f_rel_pkg}"
            diff_command = f"diff -q {f_path_src} {f_path_pkg}"
            status, _, _ = utilities.execute_command(diff_command)
            if int(status) != 0:
                modified_file_list.append((f_rel, f_path_pkg, f_path_src))
    for f in modified_file_list:
        emitter.normal(f"\t\t\t{f[0]}")
    return modified_file_list


def detect_new_files(interested_files, dir_pkg):
    emitter.sub_sub_title("detecting new files")
    new_list = []
    for f_type in interested_files:
        emitter.normal(f"\t\t{f_type}")
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
                new_list.append(f"{dir_pkg}{prefix_pkg}{f_path}")
                emitter.error(f"\t\t\t {f_path}")
        if extra_file_count == 0:
            emitter.success("\t\t\tno extra file detected")
    return new_list


def detect_suspicious_modifications(mod_files):
    emitter.sub_sub_title("detecting suspicious modifications")
    suspicious_file_list = []
    for mod_f in mod_files:
        rel_f, f_pkg, f_src = mod_f
        status_pkg = transform.upgrade_python_3(f_pkg)
        status_src = transform.upgrade_python_3(f_src)
        if int(status_src) != 0 or int(status_pkg) != 0:
            emitter.error(f"\t\tpython upgrade failed {f_pkg}, {f_src}")
        status_pkg = transform.refactor_python(f_pkg)
        status_src = transform.refactor_python(f_src)
        if int(status_src) != 0 or int(status_pkg) != 0:
            emitter.error(f"\t\tpython refactoring failed {f_pkg}, {f_src}")

        parsed_pkg, _ = transform.parse_ast(f_pkg)
        parsed_src, _ = transform.parse_ast(f_src)
        if not parsed_pkg or not parsed_src:
            emitter.error(f"\t\tpython parsing failed {f_pkg}, {f_src}")

        ast_diff_script = transform.generate_ast_diff(f_src, f_pkg)
        action_cluster_list = []
        action_cluster = []
        with open(ast_diff_script, 'r') as script_file:
            diff_command_list = script_file.readlines()
            for l in diff_command_list:
                if "New cluster" in l:
                    if action_cluster:
                        action_cluster_list.append(action_cluster)
                    action_cluster = []
                elif any(f in l for f in ["cluster type", "===", "------"]):
                    continue
                else:
                    action_cluster.append(l)
            action_cluster_list.append(action_cluster)

        for action_cluster in action_cluster_list:
            action_type = None
            is_suspicious = oracle.is_cluster_suspicious(action_cluster)
            if is_suspicious:
                if f_pkg not in suspicious_file_list:
                    suspicious_file_list.append(f_pkg)

    return suspicious_file_list


def detect_suspicious_additions(new_files):
    emitter.sub_sub_title("detecting suspicious additions")
    suspicious_file_list = []
    for f_pkg in new_files:
        if ".py" not in f_pkg:
            continue
        status_pkg = transform.upgrade_python_3(f_pkg)
        if int(status_pkg) != 0:
            emitter.error(f"\t\tpython upgrade failed {f_pkg}")
        status_pkg = transform.refactor_python(f_pkg)
        if int(status_pkg) != 0:
            emitter.error(f"\t\tpython refactoring failed {f_pkg}")
        parsed_pkg, _ = transform.parse_ast(f_pkg)
        if not parsed_pkg:
            emitter.error(f"\t\tpython parsing failed {f_pkg}")

        ast_file = transform.parse_ast(f_pkg)
        is_suspicious = oracle.is_ast_suspicious(ast_file)
        if is_suspicious:
            if f_pkg not in suspicious_file_list:
                suspicious_file_list.append(f_pkg)

    return suspicious_file_list


def analyze_files(dir_pkg, dir_src):
    emitter.sub_title("Analysing Files")
    interested_files = analyze_file_types(dir_pkg, dir_src)
    src_pyc_list, pkg_pyc_list = decompile.decompile_python_files(dir_pkg, dir_src)
    interested_files["decompiled pyc"] = {"src": src_pyc_list, "pkg": pkg_pyc_list}
    new_list = detect_new_files(interested_files, dir_pkg)
    mod_list = detect_modified_source_files(interested_files, dir_src, dir_pkg)
    suspicious_new_files = detect_suspicious_additions(new_list)
    suspicious_mod_files = detect_suspicious_modifications(mod_list)
    suspicious_files = suspicious_mod_files + suspicious_new_files

    for f in suspicious_files:
        emitter.error(f"\t\t{f}")







