import os.path
from app.core import values, utilities, emitter


def decompress_archive(archive_path, file_extension, dir_path):
    emitter.normal("\t\tdecompressing file")
    emitter.highlight(f"\t\t\tFile Path: {archive_path}")
    emitter.highlight(f"\t\t\t\tFile Extension: {file_extension}")
    emitter.highlight(f"\t\t\t\tTarget Dir: {dir_path}")
    try:
        if file_extension in ["conda", "whl"]:
            utilities.execute_command(f"unzip -o {archive_path} -d {dir_path}")
        elif file_extension in ["gz", "bz2", "zst"]:
            if dir_path:
                utilities.execute_command(f"mkdir -p {dir_path}")
                utilities.execute_command(f"tar --overwrite -xf {archive_path} -C {dir_path}")
        else:
            utilities.error_exit(f"unknown archive type: {file_extension} in {archive_path}")
    except Exception as ex:
        utilities.error_exit(f"error decompressing archive of type: {file_extension} in {archive_path}")
    return dir_path


def find_compressed(dir_path):
    emitter.normal("\t\tsearching for compressed files")
    file_list = utilities.list_dir(dir_path)
    archive_list = []
    for f_path in file_list:
        f_info = utilities.get_file_info(f_path)
        if " compressed " in f_info:
            archive_list.append(f_path)
    return archive_list


