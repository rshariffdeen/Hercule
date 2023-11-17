import os
from app.core import values
from app.core import emitter
from app.core import extract
from app.core import decompile
from app.core import utilities
from app.core import transform
from app.core import oracle
from app.tools import bandit
from app.tools import codeql
from app.tools import depclosure
from app.core import reader


def analyze_file_types(dir_pkg, dir_src):
    emitter.sub_sub_title("analysing package files")
    pkg_file_types = extract.extract_file_types(dir_pkg)
    values.result["general"]["total-files"] = sum(len(pkg_file_types[x]) for x in pkg_file_types)
    values.result["general"]["total-python-files"] = sum(len(pkg_file_types[x])
                                                         for x in pkg_file_types
                                                         if "python script" in x.lower())
    values.result["general"]["total-file-types"] = len(pkg_file_types)
    # values.result["file-types"] = dict()
    # for _type in pkg_file_types:
    #     values.result["file-types"][_type] = len(pkg_file_types[_type])
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
    src_files = []
    pkg_files = []
    for f_type in interested_files:
        if f_type in ["POSIX shell script"]:
            continue
        src_files += interested_files[f_type]["src"]
        pkg_files += interested_files[f_type]["pkg"]
    prefix_pkg = extract.extract_path_prefix(pkg_files)
    prefix_src = extract.extract_path_prefix(src_files)
    for f_rel_pkg in pkg_files:
        f_rel = f_rel_pkg.replace(prefix_pkg, "")
        f_rel_src = f"{prefix_src}{f_rel}"
        if ".py" not in f_rel:
            continue
        if f_rel_src not in src_files:
            f_rel_src = find_matching_file(f_rel, src_files)
            if f_rel_src is None:
                continue

        f_path_src = f"{dir_src}{f_rel_src}"
        f_path_pkg = f"{dir_pkg}{f_rel_pkg}"
        diff_command = f"diff -q \"{f_path_src}\" \"{f_path_pkg}\""
        status, _, _ = utilities.execute_command(diff_command)
        if int(status) != 0:
            modified_file_list.append((f_rel, f_path_pkg, f_path_src))
    for f in modified_file_list:
        emitter.normal(f"\t\t\t{f[0]}")
    return modified_file_list


def find_matching_file(src_file, search_list):
    file_name = str(src_file).split("/")[-1]
    exact_name_list = [x for x in search_list if file_name in x]
    if not exact_name_list:
        return None
    if len(exact_name_list) == 1:
        return exact_name_list[0]
    similar_list = []
    for _f in exact_name_list:
        _f_dist = utilities.levenshtein_distance(_f, src_file)
        similar_list.append((_f, _f_dist))
    sorted_list = sorted(similar_list, key=lambda x:x[1])
    return sorted_list[0][0]


def detect_new_files(interested_files, dir_pkg):
    emitter.sub_sub_title("detecting new files")
    new_list = []
    src_files = []
    pkg_files = []
    for f_type in interested_files:
        src_files += interested_files[f_type]["src"]
        pkg_files += interested_files[f_type]["pkg"]
    prefix_pkg = extract.extract_path_prefix(pkg_files)
    prefix_src = extract.extract_path_prefix(src_files)
    rel_path_list_pkg = [str(p).replace(prefix_pkg, "", 1) for p in pkg_files]
    rel_path_list_src = [str(p).replace(prefix_src, "", 1) for p in src_files]
    extra_file_count = 0
    for f_path in rel_path_list_pkg:
        if f_path not in rel_path_list_src:
            if any(_type in f_path for _type in [".bak", ".ast"]):
                continue
            if ".pyc" in f_path:
                f_path = f_path.replace(".pyc", ".pyc.py")
                abs_path = f"{dir_pkg}{prefix_pkg}{f_path}"
                if not os.path.isfile(abs_path):
                    continue
            matching_file = find_matching_file(f_path, rel_path_list_src)
            if matching_file:
                continue
            extra_file_count += 1
            new_list.append(f"{dir_pkg}{prefix_pkg}{f_path}")
            emitter.error(f"\t\t\t {f_path}")
    if extra_file_count == 0:
        emitter.success("\t\t\tno extra file detected")
    return new_list


def detect_suspicious_modifications(mod_files, dir_pkg):
    emitter.sub_sub_title("detecting suspicious modifications")
    suspicious_file_list = []
    suspicious_loc_list = []
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
            if action_cluster:
                is_suspicious, action_type = oracle.is_cluster_suspicious(action_cluster)
                if is_suspicious:
                    if f_pkg not in suspicious_file_list:
                        suspicious_file_list.append(f_pkg)
                    import_line_list = extract.extract_import_lines(action_cluster)
                    for line in import_line_list:
                        alert = f"{f_pkg}:{line} - {action_type}:import packages"
                        suspicious_loc_list.append(alert)
                    func_call_list = extract.extract_function_call_lines(action_cluster)
                    for (line, _) in func_call_list:
                        alert = f"{f_pkg}:{line} - {action_type}: function call"
                        suspicious_loc_list.append(alert)

    emitter.normal("\t\tsuspicious modified files")
    for f in suspicious_file_list:
        emitter.error(f"\t\t\t{f}")
    if not suspicious_file_list:
        emitter.error(f"\t\t\t-none-")

    emitter.normal("\t\tsuspicious locations and reasons")
    for f in suspicious_loc_list:
        _f = f.replace(dir_pkg, "")
        emitter.error(f"\t\t\t{_f}")
    if not suspicious_loc_list:
        emitter.error(f"\t\t\t-none-")

    return suspicious_file_list, suspicious_loc_list


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

    emitter.normal("\t\tsuspicious additions")
    for f in suspicious_file_list:
        emitter.error(f"\t\t\t{f}")
    if not suspicious_file_list:
        emitter.error(f"\t\t\t-none-")
    return suspicious_file_list


def analyze_loc(dir_pkg):
    emitter.sub_sub_title("analysing lines of code")
    cloc_info = dict()
    cloc_command = f"cloc --json --out {dir_pkg}/cloc.json {dir_pkg}"
    utilities.execute_command(cloc_command)
    pkg_loc_info = reader.read_json(f"{dir_pkg}/cloc.json")
    cloc_info["total-files"] = pkg_loc_info["header"]["n_files"]
    cloc_info["total-lines"] = pkg_loc_info["header"]["n_lines"]
    cloc_info["python-files"] = pkg_loc_info["Python"]["nFiles"]
    cloc_info["python-lines"] = pkg_loc_info["Python"]["code"]
    values.result["cloc"] = cloc_info


def generate_closure(dir_pkg):
    depclosure.generate_closure(dir_pkg)


def behaviour_analysis(dir_pkg):
    emitter.sub_sub_title("detecting malicious behavior")
    emitter.normal("\t\tcreating codeql database")
    codeql.generate_codeql_database(dir_pkg)

    emitter.normal("\t\trunning queries against codeql database")
    codeql_results = codeql.generate_codeql_query_report(dir_pkg)
    codeql.remove_database(dir_pkg)
    # values.result["codeql-analysis"] = codeql_results
    codeql_alerts = codeql_results["runs"][0]["results"]

    setup_py_alerts = []
    malicious_files = set()
    for alert in codeql_alerts:
        locations = alert["locations"]
        for loc in locations:
            _loc = loc["physicalLocation"]["artifactLocation"]["uri"]
            if "setup.py" in _loc:
                setup_py_alerts.append(_loc)
            malicious_files.add(_loc)

    if codeql_alerts:
        values.result["has-malicious-behavior"] = True

    emitter.normal("\t\tmalicious files")
    if not malicious_files:
        emitter.error(f"\t\t\t-none-")
    for f in malicious_files:
        _f = f.replace(dir_pkg, "")
        emitter.error(f"\t\t\t{_f}")

    values.result["codeql-analysis"] = dict()
    values.result["codeql-analysis"]["setup-hercule-alerts"] = len(setup_py_alerts)
    values.result["codeql-analysis"]["hercule-alerts"] = len(codeql_alerts)
    values.result["codeql-analysis"]["hercule-report"] = codeql_alerts
    values.result["codeql-analysis"]["malicious-file-count"] = len(malicious_files)
    values.result["codeql-analysis"]["malicious-files"] = list(malicious_files)


def analyze_files(dir_pkg, dir_src):
    interested_files = analyze_file_types(dir_pkg, dir_src)
    analyze_loc(dir_pkg)
    src_pyc_list, pkg_pyc_list = decompile.decompile_python_files(dir_pkg, dir_src)
    interested_files["decompiled pyc"] = {"src": src_pyc_list, "pkg": pkg_pyc_list}
    new_list = detect_new_files(interested_files, dir_pkg)
    mod_list = detect_modified_source_files(interested_files, dir_src, dir_pkg)
    values.result["general"]["total-modified-files"] = len(mod_list)
    values.result["general"]["total-new-files"] = len(new_list)
    suspicious_new_files = detect_suspicious_additions(new_list)
    suspicious_mod_files, suspicious_mod_locs = detect_suspicious_modifications(mod_list, dir_pkg)
    suspicious_files = suspicious_mod_files + suspicious_new_files
    values.result["general"]["suspicious-modified-files"] = len(suspicious_mod_files)
    values.result["general"]["suspicious-new-files"] = len(suspicious_new_files)
    values.result["general"]["total-suspicious-files"] = len(suspicious_files)
    values.result["general"]["total-suspicious-modifications"] = len(suspicious_mod_locs)
    values.result["suspicious-files"] = ",".join(suspicious_files)
    values.result["suspicious-modifications"] = ",".join(suspicious_mod_locs)
    if not suspicious_files:
        values.result["has-integrity"] = True
    whole_pkg_res = bandit.generate_bandit_dir_report(dir_pkg)
    whole_src_res = bandit.generate_bandit_dir_report(dir_src)
    whole_pkg_alerts = whole_pkg_res.get("results", [])
    whole_src_alerts = whole_src_res.get("results", [])
    setup_py_pkg_alerts = [x for x in whole_pkg_alerts if "setup.py" in x["filename"]]
    setup_py_src_alerts = [x for x in whole_src_alerts if "setup.py" in x["filename"]]
    hercule_alerts = []
    for f in suspicious_files:
        f_result = bandit.generate_bandit_source_report(f)
        if not f_result:
            continue
        f_locs = []
        if f in suspicious_mod_files:
            for loc in suspicious_mod_locs:
                if f in loc:
                    f_locs.append(loc)
            f_result_filtered = bandit.filter_alerts(f_result, f_locs)
            hercule_alerts += f_result_filtered
        else:
            hercule_alerts += f_result["results"]
    setup_py_hercule_alerts = [x for x in hercule_alerts if "setup.py" in x["filename"]]
    values.result["has-malicious-code"] = False
    if hercule_alerts:
        values.result["has-malicious-code"] = True

    values.result["bandit-analysis"]["whole-pkg-alerts"] = len(whole_pkg_alerts)
    values.result["bandit-analysis"]["whole-src-alerts"] = len(whole_src_alerts)
    values.result["bandit-analysis"]["setup-pkg-alerts"] = len(setup_py_pkg_alerts)
    values.result["bandit-analysis"]["setup-src-alerts"] = len(setup_py_src_alerts)

    values.result["bandit-analysis"]["filtered-setup-alerts"] = len(setup_py_hercule_alerts)
    values.result["bandit-analysis"]["filtered-alerts"] = len(hercule_alerts)
    values.result["bandit-analysis"]["filtered-report"] = hercule_alerts


def final_result():
    emitter.sub_sub_title("Analysis Results")
    emitter.normal("\t\tIntegrity")
    emitter.highlight(f"\t\t\thas-integrity: {values.result['has-integrity']}")
    emitter.highlight(f"\t\t\tsuspicious source file additions: {values.result['general']['suspicious-new-files']}")
    emitter.highlight(f"\t\t\tsuspicious source file modifications: { values.result['general']['suspicious-modified-files']}")
    emitter.highlight(f"\t\t\tsuspicious source location modifications: {values.result['general']['total-suspicious-modifications']}")

    emitter.normal("\t\tMalicious Code Segments (Bandit4Mal)")
    emitter.highlight(f"\t\t\thas-malicious-code: {values.result['has-malicious-code']}")
    emitter.highlight(f"\t\t\tpackage alerts: {values.result['bandit-analysis']['whole-pkg-alerts']}")
    emitter.highlight(f"\t\t\tsource alerts: {values.result['bandit-analysis']['whole-src-alerts']}")
    emitter.highlight(f"\t\t\tfiltered alerts: {values.result['bandit-analysis']['filtered-alerts']}")

    emitter.normal("\t\tMalicious Code Segments (Code4QL)")
    emitter.highlight(f"\t\t\thas-malicious-behavior: {values.result['has-malicious-behavior']}")
    emitter.highlight(f"\t\t\tmalicious behavior alerts: {values.result['codeql-analysis']['hercule-alerts']}")
    emitter.highlight(f"\t\t\tmalicious behavior files: { values.result['codeql-analysis']['malicious-file-count']}")
    emitter.highlight(f"\t\t\tmalicious alerts in setup: {values.result['codeql-analysis']['setup-hercule-alerts']}")












