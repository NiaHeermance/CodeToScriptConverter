# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# CodeToScriptConverter.py
# Nia~
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

import sys

from Code.script_writer import ScriptWriter
from Config.Files.filenames_to_document_titles import get_document_title


def main():
    arguments = get_command_line_arguments()
    arguments = sys.argv[1:]


def get_command_line_arguments():
    if len(sys.argv) == 1:
        message = """Error: Incorrect number of arguments.

        Either provide a directory for files to convert,
        a list of files to convert separated by spaces,
        or --use-input-dir to convert all files in the Input folder.
        """
        print(message)
        exit()


if __name__ == "__main__":
    main()
