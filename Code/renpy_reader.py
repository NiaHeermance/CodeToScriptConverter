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
import json
from enum import Enum

import Code.dialogue as dia
import Code.script_instruction as si

INDENT_FOR_BLOCK_TYPE = {
    "decision_tree": 2,
    "route_specific": 1
}


class FileLocation:
    """
    A helper object representing a location in a file.
    """
    def __init__(self, file_index: int, line_index: int):
        self.file_index = file_index
        self.line_index = line_index

class ScanLine(Enum):
    """
    An object we return to getNextScriptElement to provide information on what line to scan next
    """
    NEXT_LINE = 0
    CURRENT_LINE = 1



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
            self.rpyFile = rpy_file.readlines()
        self.__initializeTags()
        self.__initializeStyle()
        self.indent_lev = 1
        self.index = 0
        self.blocks = deque()
        self.current_block = "no_block"


    def getNextScriptElement(self) -> dia.Dialogue | si.ScriptInstruction:
        """
        Returns the next major script element. Will be dialogue or scene change related.
        """
        while True:
            if self.atEndOfFile():
                return si.EndDocument()

            line = self.rpyFile[self.index]
            if len(line) == 0 or line.isspace():
                self.index += 1
                continue

            # Update indent of read head if leaving a code block in the rpy file.
            if len(self.blocks) > 0:
                __checkIfExitBlock(line)
            
            # Remove spacing and unnecessary tags at the start of a line
            line = __removeInitialFront(line)
            if line == "skip":
                self.index += 1
                continue

            # Check character match
            result = self.__characterMatch(line)
            if not (result is None):
                self.index += 1
                return result
            
            # Check for high priority tags match
            result = self.__lookForTags(line, self.tags)
            if isinstance(result, ScanLine):
                if result == ScanLine.NEXT_LINE:
                    self.index += 1
                continue
            if not (result is None):
                self.index += 1
                return result

            # Then pass over tags we are told to ignore
            result = self.__lookForTags(line, self.toIgnore)
            if result == ScanLine.NEXT_LINE:
                self.index += 1
                continue

            # Finally look for low priority tags
            result = self.__lookForTags(line, self.lowPriorityTags)
             if isinstance(result, ScanLine):
                if result == ScanLine.NEXT_LINE:
                    self.index += 1
                continue
            if not (result is None):
                self.index += 1
                return result

            print(f'Error: Tag in line {line} not recognized.')
            self.index += 1
            continue


    
    def atEndOfFile(self) -> bool:
        """
        Returns true if the last read line was the end of the provided file.
        """
        return self.index >= len(self.rpyFile)


    # ---------------------------------

    # ----
    # Private Functions
    # ----

    # Initalization
    # -------------

    def __initializeTags(self):
        """
        Initializes tag member variables we will then scan for in the rpy file.
        """
        with open("../Config/Files/tags_to_script.json", "r") as tags_to_script_file:
            tags_to_script = json.load(tags_to_script_file)

            self.indent = tags_to_script["Indent Type"]
            self.initialFronts = tags_to_script["Initial Fronts"]
            self.mainCharacters = tags_to_script["Main Characters"]
            self.tags = tags_to_script["Tags"]
            self.toIgnore = tags_to_script["To Ignore"]
            self.lowPriorityTags = tags_to_script["Low Priority Tags"]

            self.nontagMainCharacters = []
            def checkForCharacterTags(tags):
                for tag, tag_info in tags:
                    if "Character" in tag_info and tag[0].isalpha():
                        self.nontagMainCharacters.append(tag)
            checkForCharacterTags(self.tags)
            checkForCharacterTags(self.lowPriorityTags)


    def __initializeStyle(self):
        """
        Initializes a style guide so that we know what formatting to use for different
        kinds of dialogue.
        """
        with open("../Config/Files/style_guide.json", "r") as style_guide_file:
            self.styleGuide = json.load(style_guide_file)


    # ---


    # Initial Line Processing
    # -----------------------

    def __checkIfExitBlock(self, line: str):
        """
        Checks if the indention is so much less than self.indent_lev that we must have
        exited from a choice prompt section or an path-exlclusive if-statement.
        
        line -- current line we're investigating its indent
        """
        indent_spot = self.indent_lev * len(self.indent)
        if indent_spot < 0 or len(self.blocks) == 0:
            return

        chunk_before = line[:indent_spot]
        if not chunk_before.isspace(): # Assumes indent_type is whitespace
            block_we_leave = self.blocks.pop()
            self.indent_lev -= INDENT_FOR_BLOCK_TYPE[block_we_leave]
            if len(self.blocks()) > 0:
                self.current_block = self.blocks[-1]
            else:
                self.current_block = "no_block"


    def __removeInitialFront(self, line: str) -> str:
        """
        Given a string line, removes any front found in self.initialFronts
        Also removes spaces based on self.indent level

        line -- line to remove a starting front from as well as indentation
        return: trimmed string
        """
        indent_spot = self.indent_lev * len(self.indent)
        chunk_before = line[:indent_spot]
        if not chunk_before.isspace():
            if self.current_block == "decision_tree":
                return "skip" # This is a menu option header, and we want to look inside menu options instead
            else:
                line = line[indent_spot - len(self.indent):] # Might need more indents. Also not sure yet what this code is for.
        else:
            line = line[indent_spot:]

        for front in self.initialFronts:
            if line.startswith(front):
                return line[len(front):]
        return line


    # ---


    # Tag Matching
    # --------------

    def __lookForTags(self, line: str, tags: dict) -> dia.Dialogue | ScanLine | si.ScriptInstruction:
        for tag in self.tags.keys():
            result = self.__isTagMatch(self, line, self.index, tag)
            if result is None:
                continue
            if self.index != result.file_index:
                self.index = result.file_index
                line = self.rpyFile[result.file_index][result.line_index:]
            else:
                line = line[len(tag):]

            tag_info = self.tags[tag]
            mode = tag_info["Mode"]

            if mode == "non_main_character":
                return self.__scriptLine(self.most_recent_non_main_character, line)

            if mode == "show_block":
                self.__handleShowBlock(line)
                return ScanNextLine.NEXT_LINE

            if mode in {"narration", "prose_narration", "thought", "dialogue", "scene_header"}:
                style = getattr(dia.TextStyle, styleGuide[mode].upper())
                return self.__scriptLine(tag_info.character, line, style)

            if mode == "scene_header":
                return self.__sceneTransition(line, tag_info["Type"])

            if mode == "d"

    def __isTagMatch(self, processed_line: str, file_index: int, tag: str) -> FileLocation:
        """
        Returns true if processed_line.startswith(tag), allowing for new line characters in tag.
        If \n in tag, then we look at the next line instead of processed_line. Note that we do not
        remove the initial front on this new line.

        processed_line - String that we are comparing against.
        file_index     - Index of processed_line in rpyFile in case we need to check the next lint
        tag            - Tag we are comparing against.
        return: None if not a match, the FileLocation of where parsing should pick up if match
        """
        tag_index = 0
        line = processed_line
        line_index = 0
        matching = True
        while matching and tag_index < len(tag):
            if tag[tag_index] == "\n":
                file_index += 1
                line = self.rpyFile[file_index]
                line_index = 0
                tag_index += 1
                continue
            if line_index >= len(line):
                matching = False
                break
            if line[line_index] != tag[tag_index]:
                matching = False
            
            line_index += 1
            tag_index += 1

        if matching:
            return FileLocation(file_index, line_index)
        return None


    def __characterMatch(self, line: str) -> dia.Dialogue:
        """
        Given a line in a rpy file, returns the dialogue on that line if the character is one of our main characters.
        """
        capitalized_line = line.capitalize()
        for name in self.mainCharacters.keys():
            if capitalized_line.startswith(name):
                line = line[len(name):]
                return __scriptLine(name, line)
        return None


    # ---


    # Tag Responders
    # --------------

    def __scriptLine(self, character: str, line: str, style: dia.TextStyle = dia.TextStyle.NORMAL) -> dia.Dialogue:
        """
        Returns a dialogue object so a ScriptWriter can understand what to print to a script.
        """
        line = line.replace("\"", "").strip()
        if self.new_path:
            self.new_path = False
            return dia.Dialogue(character, line, style, True, self.path_reason)
        return dia.Dialogue(character, line, style, self.exclusive_lines)
        # TODO IF ALT IMPLEMENTED, THEN MAKE SURE LISTS IN LATEX RESUMES NUMBERING.


    def __handleShowBlock(self, line: str):
        """
        Records if the showed character is a non-main-character so that we know the name of them if they speak.
        Then skips ahead in file until we're out of the show block.
        """
        character = line.split()[0]
        if character in self.mainCharacters or character in self.nontagMainCharacters:
            self.most_recent_non_main_character = character

        # Now skipping show block.
        self.index += 1
        indentLocation = self.indent_lev * len(self.indent)
        while self.rpyFile[self.index][indentLocation+1].isspace():
            self.index += 1


    def __sceneTransition(self, line: str, labelType: str) -> NewScene:
        """
        Given a processed line in the rpy file, return the new scene's name.

        line      - The line at self.rpyFile with the front of it removed.
        labelType - Either "label" or "comment". This is the type of rpy line that the new scene's name is on.
        return: A NewScene object with the scene's correct name.
        """
        if labelType == "label":
            line = self.rpyFile[self.index]
            index = line.index("label")
            line = line[index + len("label"):]
        return si.NewScene(line.strip())


