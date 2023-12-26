# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# CodeToScriptConverter.py
# Nia~
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

import sys
import os
import glob

from Code.script_writer import ScriptWriter
from Config.Files.filenames_to_document_titles import get_document_title

def main():
    arguments = get_command_line_arguments()
    to_convert = get_files_to_convert(arguments)

    


# --------------------------------------------

# ----
# Processing command-line arguments
# ----

def get_command_line_arguments():
    """
    Returns command-line arguments, not including the initial file name.
    Prints a message if wrong number of arguments.
    """
    if len(sys.argv) == 1:
        message ="""Error: Incorrect number of arguments.

Either provide directories and/or individual rpy files to create scripts from,
or --use-input-dir to convert all files in the Input folder.
        """
        print(message)
        exit()

    return sys.argv[1:]


def get_files_to_convert(arguments: list) -> list:
    """
    Given a list of paths and/or --use-input-dir,
    returns all files in those locations in a list.

    The list of paths can include a mix of directories and single files.
    """
    ret = []
    for path in arguments:
        if path == "--use-input-dir":
            arguments.append("Input")
            continue

        if not os.path.exists(path):
            message = f"""Error: Path {path} does not exist.

Please check that the path was written properly.
"""
            print(message)
            exit()

        if os.path.isdir(path):
            current_path = os.getcwd()
            os.chdir(path)
            ret.extend(glob.glob("**/*.rpy", recursive=True))
            os.chdir(current_path)
        elif path.endswith(".rpy"):
            ret.append(path)
    return ret


# --------------------------------------------




if __name__ == "__main__":
    main()