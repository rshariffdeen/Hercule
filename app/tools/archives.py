import os.path
from app.core import values, utilities, emitter


def decompress_archive(archive_path):
    emitter.normal("\t\t\tdecompressing file")
    archive_name = str(archive_path).split("/")[-1]
    file_extension = archive_name.split(".")[-1]
    dir_path = f"{values.dir_experiments}/{archive_name}-dir"
    emitter.highlight(f"\t\t\t\tFile Extension: {file_extension}")
    emitter.highlight(f"\t\t\t\tTarget Dir: {dir_path}")
    try:
        if file_extension in ["conda", "whl"]:
            utilities.execute_command(f"unzip {archive_path} -d {dir_path}")
        elif file_extension in ["gz", "bz2"]:
            utilities.execute_command(f"mkdir -p {dir_path}")
            utilities.execute_command(f"tar -xf {archive_path} -C {dir_path}")
        else:
            utilities.error_exit(f"unknown archive type: {file_extension} in {archive_path}")
    except Exception as ex:
        utilities.error_exit(f"error decompressing archive of type: {file_extension} in {archive_path}")


def find_compressed(dir_path):
    file_list = utilities.list_dir(dir_path)
    archive_list = []
    for f_path in file_list:
        f_info = utilities.get_file_info(f_path)
        if " compressed " in f_info:
            archive_list.append(f_path)
    return archive_list


