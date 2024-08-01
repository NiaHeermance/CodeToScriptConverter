# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# CodeToScriptConverter.py
# Nia~
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

# Python Libraries
import sys
from pathlib import Path
from os import listdir
from textwrap import dedent

# Custom code
from Code.script_writer import ScriptWriter
from Config.Files.filenames_to_document_titles import get_document_title
from Code.renpy_reader import RenpyReader
import Code.script_instruction as si


# -------------------------------

# ----
# Functions
# ----


def main():
	files = getFilesFromCommandLine()
	for file in files:
		createScript(file)


# ----


# Command Line Processing
# ----------------

def getFilesFromCommandLine() -> list[Path]:
	"""
	Process the command line arguments and returns the .rpy files to convert into PDF scripts.

	Try --usage to see how to use this script.
	"""
	if len(sys.argv) == 1:
		message = dedent("""\
			No arguments provided. Will convert files in Input dir instead.
			For usage, add --usage
		""")
		print(message)
		answer = ""
		while (answer != "Y" and answer != "N"):
			answer = input("Is this alright? (Y/N) ")
		if answer == "N":
			exit()
		return getRpyFilesInDir("Input/")

	if sys.argv[1] == "--usage":
		usage = dedent("""\
			Usage:
			Either provide a directory for files to convert
			or a list of files to convert separated by spaces.

			If not argument is provided, files in the Input dir are converted.
		""")
		print(usage)
		exit()

	if len(sys.argv) == 2:
		path = Path(sys.argv[1])
		if not path.exists():
			error = f"Error: The string {sys.argv[1]} is not a valid path. Try --usage."
			print(error)
			exit()

		if path.is_dir():
			return getRpyFilesInDir(path)
		if not path.suffix == ".rpy":
			error = f"Error: {path.as_posix()} is not a .rpy file."
			print(error)
			exit()
		return [path]
	
	else:
		ret = []
		for argument in sys.argv[1:]:
			path = Path(argument)
			if not path.exists() or not path.suffix.endswith(".rpy"):
				error = f"Error: File {path.as_posix()} is not a valid .rpy file."
				print(error)
				exit()
			ret.append(path)
		return ret


def getRpyFilesInDir(path: str|Path) -> list[Path]:
	"""
	Given a directory path or string, returns all rpy files as Path objects in dir

	path - str or Path of a directory
	return: All .rpy files in the location.
	"""
	ret = [Path(file) for file in listdir(path) if file.endswith(".rpy")]
	if len(ret) == 0:
		error = f"Error: No .rpy files in {str(path)}."
		print(error)
		exit()
	return ret


# ---


# Script Creation
# ---------------

def createScript(file: Path)
	"""
	Creates a PDF script from a file path to an rpy file.
	"""
	output_filename = get_document_title(file.name)
	
	script_writer = ScriptWriter(output_filename)
	script_writer.beginDocument(output_filename)

	renpy_reader = RenpyReader(file.as_posix())

	in_scene = False
	while not renpy_reader.atEndOfFile():
		response = renpy_reader.getNextScriptElement()
		if isinstance(response, si.EndScene):
			break
		if isinstance(response, si.NewScene):
			if in_scene:
				script_writer.EndScene()
			in_scene = True
			script_writer.beginScene(response.sceneName)
		if isinstance(response, dia.Dialogue):
			if response.path_exclusive:
				script_writer.addPathExclusiveLine(
					response.character,
					response.line,
					response.style,
					response.path_reason
				)
			else:
				script_writer.addLine(response.character, response.line, response.style)
		
	if in_scene:
		script_writer.EndScene()
	
	script_writer.endDocument()
	script_writer.renderDocument()


if __name__ == "__main__":
	main()