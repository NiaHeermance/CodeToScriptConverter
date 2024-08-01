# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# script_writer.py
# Nia~
#
# This class ScriptWriter can create PDF scripts with an easy API.
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

from io import StringIO
import re

import Code.doc_format as doc_format
from Code.dialogue import TextStyle


def convertToFormat(text: str):
        """
        Returns the provided text replacing {tags}{/tags}
        with the format specified in doc_format
        """
        if not hasattr(convertToFormat, "alreadyRun"):
            tagToFunc = {
                "b": "bold",
                "i": "italics",
                "u": "underline",
                "q": "quote"
            }

            tagToReplace = {}
            for tag, name in tagToFunc.items():
                tagToReplace[f'{{{tag}}}'] = getattr(doc_format, f'{name}Left')()
                tagToReplace[f'{{\\{tag}}}'] = getattr(doc_format, f'{name}Right')()
            # Required because our keys have meta characters
            convertToFormat.tagToReplace = {re.escape(key): value for key, value in tagToReplace.items()}
            
            # | as we want to match to any of them
            convertToFormat.pattern = re.compile( "|".join( convertToFormat.tagToReplace.keys() ) )

            convertToFormat.alreadyRun = True

        def onMatch(match: re.Match):
            return convertToFormat.tagToReplace[re.escape(match.group(0))]

        return convertToFormat.pattern.sub(onMatch, text)


class ScriptWriter:
    # ----
    # Methods
    # ----

    def __init__(self, file_name: str, putInTestOutput: bool = False):
        """
        Sets up a ScriptWriter object to be able to add lines to a document.

        file_name - The name of the file we are creating.
        """
        self.in_exclusive_lines = False
        self.scene_count = 1

        self.scene_characters = set()
        self.document_characters = set()

        self.scene_buffer = StringIO()
        self.document_buffer = StringIO()
        if putInTestOutput
            self.output_file_path = f'../Output/{file_name}.tex'
        else:
            self.output_file_path = f'../Tests/TestOutput/{file_name}.tex'
        self.output_file = open(self.output_file_path, "w")


    def addLine(self, character: str, text: str, style: TextStyle):
        """
        Adds a line to the script.
        character -- Name of character saying the line.
        text      -- Text in line
        style     -- Way line is written. "normal, "bold," "italic," "underline," and "quote."
        """
        if self.in_exclusive_lines:
            self.__endPathExclusiveLines()
        self.__writeLine(character, text, style)


    def addPathExclusiveLine(self, character: str, text: str, style: TextStyle, reason: str = ""):
        """
        Adds a path-exclusive line to the script.
        character -- Name of character saying the line.
        text      -- Text in line
        style     -- Way line is written. "normal", "bold," "italic," "underline," and "quote."
        reason    -- Make non-empty or "NEW" to specify a new list of exclusive lines.
        """
        if not self.in_exclusive_lines:
            self.__beginPathExclusiveLines(reason)
        elif reason != "":
            self.__beginSingularPathLines(reason)

        self.__writeLine(character, text, style, buffer = self.exclusive_lines[self.path_index])


    def beginDocument(self, name: str):
        """ 
        Begins a document with title "name."

        name -- Title of document, not the fle name.
        """
        self.output_file.write(doc_format.document_format_start())
        self.output_file.write(doc_format.bold(name) + "\n\n")


    def beginScene(self, scene_name: str):
        """
        Begins a scene with name "scene_name."

        scene_name -- Name of the scene used in header.
        """
        self.scene_buffer = StringIO()
        self.scene_characters.clear()

        text = doc_format.bold(f'Scene {self.scene_count}, {scene_name}')
        self.scene_count += 1
        self.document_buffer.write(f'\n{text}\n\n')
        
        self.scene_buffer.write(doc_format.start_list("number"))


    def endScene(self):
        """
        Does the necessary formatting to end a scene.
        """
        if self.in_exclusive_lines:
            self.__endPathExclusiveLines()
        self.scene_buffer.write(doc_format.end_list())

        self.__writeCharacterList(self.document_buffer, list(self.scene_characters))
        self.scene_buffer.seek(0)
        self.document_buffer.write(self.scene_buffer.read())
        self.scene_buffer.close()

        self.document_characters.update(self.scene_characters)


    def endDocument(self):
        """
        Pushes the buffer to the document and saves the file.
        """
        self.__writeCharacterList(self.output_file, list(self.document_characters), True)
        self.document_buffer.seek(0)
        self.output_file.write(self.document_buffer.read())
        self.output_file.write(doc_format.document_format_end())

        self.document_buffer.close()
        self.output_file.close()


    def renderDocument(self):
        """
        Renders the document into a PDF if not already so.
        Should only be called after endDocument is called.
        """
        doc_format.renderDocument(self.output_file_path)


    # ---------------------------------

    # ----
    # Private Methods
    # ----

    def __writeLine(self, character: str, text: str, style: TextStyle, buffer: StringIO = None):
        """
        Adds a line to the script. Called by other functions.

        character -- Name of character saying the line.
        text      -- Text in line
        style     -- Way line is written. "normal," "bold," "italic," "underline," and "quote."
        """
        if buffer == None:
            buffer = self.scene_buffer
        text = convertToFormat(text)
        line = f'{character}: {doc_format.get_text_with_style(text, style)}'
        buffer.write(doc_format.list_item(line))
        self.scene_characters.add(character)



    def __writeCharacterList(self, io_buffer: StringIO, characters: list, section_break: bool = False):
        """
        Prints character list to the buffer provided.
       
        io_buffer  -- Buffer to print characters to.
        characters -- List of character names to print
        """
        if len(characters) == 0:
            return
        end_space = "\n\n"
        if section_break:
            end_space = f"{doc_format.new_line()}\n\n"

        io_buffer.write(f"{doc_format.boldLeft()}Characters: ")
        characters.sort()
        for i, character in enumerate(characters):
            if i != len(characters)-1:
                io_buffer.write(f'{character}, ')
            else:
                io_buffer.write(f'{character}{doc_format.boldRight()}{end_space}')


    def __beginPathExclusiveLines(self, reason: str):
        """
        Sets up the document for adding path-exclusive lines.
        """
        self.reasons = [reason]
        self.exclusive_lines = [StringIO()]
        self.path_index = 0
        self.in_exclusive_lines = True


    def __beginSingularPathLines(self, reason: str):
        """
        Adds another path of lines to this bullet point.
        """
        self.reasons.append(reason)
        self.exclusive_lines.append(StringIO())
        self.path_index += 1


    def __endPathExclusiveLines(self):
        """
        Ends a block of path-exclusive lines.
        """
        if len(self.reasons) == 1:
            reason = self.reasons[0]
            if reason == "":
                reason = "Path:"
            self.scene_buffer.write(doc_format.list_item(reason))
            self.scene_buffer.write(doc_format.start_list("number"))
            buffer = self.exclusive_lines[0]
            buffer.seek(0)
            self.scene_buffer.write(buffer.read())
            buffer.close()

        else:
            self.scene_buffer.write(doc_format.list_item("DELETEME"))
            self.scene_buffer.write(doc_format.start_list("letter"))
            count = 1
            for reason, buffer in zip(self.reasons, self.exclusive_lines):
                if reason == "" or reason == "NEW":
                    reason = f'Path {count}'
                self.scene_buffer.write(doc_format.list_item(reason))
                self.scene_buffer.write(doc_format.start_list("number"))
                buffer.seek(0)
                self.scene_buffer.write(buffer.read())
                buffer.close()
                self.scene_buffer.write(doc_format.end_list())
                count += 1

        self.scene_buffer.write(doc_format.end_list())
        self.in_exclusive_lines = False
