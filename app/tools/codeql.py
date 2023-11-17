import os.path
from app.core import values, utilities, emitter
from app.core.utilities import execute_command
from app.core import reader
import shutil


def generate_codeql_database(dir_pkg):
    remove_database(dir_pkg)
    codeql_cmd = f"codeql database create  --language=python {values.codeql_database_name}"
    # print(codeql_cmd, " in ",dir_pkg)
    status,out,err = execute_command(codeql_cmd,directory=dir_pkg)


def remove_database(dir_pkg):
    shutil.rmtree(os.path.join(dir_pkg,values.codeql_database_name),ignore_errors=True)


def generate_codeql_query_report(dir_pkg):
    codeql_cmd = f"codeql database analyze --rerun -j 10 --format={values.codeql_output_format} --output={values.codeql_output_name} {values.codeql_database_name} {os.path.join(values.dir_main,'codeql','templates')}"
    # print(codeql_cmd, " in ",dir_pkg)
    status,out,err = utilities.execute_command(codeql_cmd,directory=dir_pkg)
    if out:
        print(out.decode())
    if err:
        print(err.decode())
    codeql_report = reader.read_json(os.path.join(dir_pkg, values.codeql_output_name))
    return codeql_report

