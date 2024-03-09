# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# renpy_reader.py
# Nia~
#
# This class RenpyReader reads renpy code line by line and provides an
# API for using this data to create a script.
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

from collections import deque

INDENT_FOR_BLOCK_TYPE = {
    "decision_tree": 2,
    "route_specific": 1
}

class RenpyReader:
    # ----
    # Member Functions
    # ----

    def __init__(self, file_path: str):
        """
        Sets up a RenpyReader object to be able to scan lines of a .rpy file.
        file_path - The path to the .rpy we will be scanning.
        """
        with open(file_path, "r") as rpy_file:
            self.rpy_file = rpy_file.readlines()
        self.__initializeTags()
        self.__initializeStyle()
        self.indent_lev = 1
        self.index = 0
        self.blocks = deque()
        self.recent_block = "no_block"


    def nextScriptChunk(self):
        if len(self.rpy_file) == 0:
            return "done"

        while not self.__atEndOfFile():
            line = self.rpy_file[self.index]

            if len(self.blocks) > 0:
                __checkIfExitBlock(line)
            
            line = __removeInitialFront(line)
            if line == "skip":
                self.index += 1
                continue

            



            for ignore in self.to_ignore:
                if line.star
        

        return "done"


    # ---------------------------------

    # ----
    # Private Functions
    # ----

    # Initializes tag member variables we will then scan for in the rpy file.
    def __initializeTags(self):
        with open("../Config/Files/tags_to_script.json", "r") as tags_to_script_file:
            tags_to_script = json.load(tags_to_script_file)

            self.indent = tags_to_script["Indent Type"]
            self.inital_fronts = tags_to_script["Initial Fronts"]
            self.main_characters = tags_to_script["Main Characters"]
            self.tags = tags_to_script["Tags"]
            self.to_ignore = tags_to_script["To Ignore"]
            self.low_priority_tags = tags_to_script["Low Priority Tags"]


    # Initializes a style guide so that we know what formatting to use for different
    # kinds of dialogue.
    def __initializeStyle(self):
        with open("../Config/Files/style_guide.json", "r") as style_guide_file:
            self.style_guide = json.load(style_guide_file)


    # Returns true if the last read line was the end of the provided file.
    def __atEndOfFile(self):
        line = self.rpy_file[self.index]
        return len(line) == 0 or line[-1] != '\n'


    # Checks if the indention is so much less than self.indent_lev that we must have
    # exited from a choice prompt section or an path-exlclusive if-statement.
    # line -- current line we're investigating its indent
    def __checkIfExitBlock(self, line: str): # TODO use if and menu stacks
        indent_spot = self.indent_lev * len(self.indent)
        if indent_spot < 0 or len(self.blocks) == 0:
            return

        chunk_before = line[:indent_spot]
        if not chunk_before.isspace():
            block_we_leave = self.blocks.pop()
            self.indent_lev -= INDENT_FOR_BLOCK_TYPE[block_we_leave]
            if len(self.blocks()) > 0:
                self.recent_block = self.blocks[-1]
                self.check_if_exit_menu(line)
            else:
                self.recent_block = "no_block"


    # Given a string line, removes any front found in self.initial_fronts
    # Also removes spaces based on self.indent level
    # line -- line to remove a starting front from as well as indentation
    # return: trimmed string
    def __removeInitialFront(self, line: str) -> str:
        indent_spot = self.indent_lev * len(self.indent)
        chunk_before = line[:indent_spot]
        if not chunk_before.isspace():
            if self.recent_block == "decision_tree":
                return "skip"
            else:
                line = line[indent_spot - len(self.indent):]
        else:
            line = line[indent_spot:]

        for front in self.inital_fronts:
            if line.startswith(front):
                return line[len(front):]
        return line