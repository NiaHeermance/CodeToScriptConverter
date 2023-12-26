# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# script_writer.py
# Nia~
#
# This class ScriptWriter can create PDF scripts with an easy API.
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

from io import StringIO
import Code.doc_format as doc_format


class ScriptWriter:
    # ----
    # Member Functions
    # ----

    def __init__(self, file_name: str):
        """
        Sets up a ScriptWriter object to be able to add lines to a document.

        file_name - The name of the file we are creating.
        """
        self.in_sublist = False
        self.scene_count = 1

        self.scene_characters = set()
        self.document_characters = set()

        self.scene_buffer = StringIO()
        self.document_buffer = StringIO()
        self.output_file_path = f"../Output/{file_name}.tex"
        self.output_file = open(self.output_file_path, "w")

    def addLine(self, character: str, text: str, style: str):
        """
        Adds a line to the script.
        character -- Name of character saying the line.
        text      -- Text in line
        style     -- Way line is written. "bold," "italic," "underline," and "quote."
        """
        if self.in_sublist:
            self.end_path_exclusive_lines()
        self.write_line(character, text, style)

    def pathExclusiveLine(self, character: str, text: str, style: str):
        """
        Adds a path-exclusive line to the script.
        character -- Name of character saying the line.
        text      -- Text in line
        style     -- Way line is written. "bold," "italic," "underline," and "quote."
        """
        if not self.in_sublist:
            self.begin_path_exclusive_lines()
        self.write_line(character, text, style)

    def writeCharacterList(self, io_buffer, characters):
        if len(characters) == 0:
            return
        io_buffer.write("Characters: ")
        for i, character in enumerate(characters):
            if i != len(characters) - 1:
                io_buffer.write(f"{character}, ")
            else:
                io_buffer.write(f"{character}\n\n")

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

        text = doc_format.bold(f"Scene {self.scene_count}, {scene_name}")
        self.scene_count += 1
        self.document_buffer.write(f"\n{text}\n\n")

        self.scene_buffer.write(doc_format.start_list("number"))

    def endScene(self):
        """
        Does the necessary formatting to end a scene.
        """
        self.scene_buffer.write(doc_format.end_list())

        self.writeCharacterList(self.document_buffer, self.scene_characters)
        self.scene_buffer.seek(0)
        self.document_buffer.write(self.scene_buffer.read())
        self.scene_buffer.close()

        self.document_characters.update(self.scene_characters)

    def endDocument(self):
        """
        Pushes the buffer to the document and saves the file.
        """
        self.writeCharacterList(self.output_file, self.document_characters)
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
    # Private Functions
    # ----

    # Adds a line to the script. Called by other functions.
    # character -- Name of character saying the line.
    # text      -- Text in line
    # style     -- Way line is written. "bold," "italic," "underline," and "quote."
    def write_line(self, character: str, text: str, style: str):
        line = f"{character}: {doc_format.get_text_with_style(text, style)}"
        self.scene_buffer.write(doc_format.list_item(line))
        self.scene_characters.add(character)

    # Sets up the document for adding path-exclusive lines.
    def begin_path_exclusive_lines(self):
        if self.in_sublist:
            self.end_path_exclusive_lines()

        self.scene_buffer.write(doc_format.list_item(""))
        self.scene_buffer.write(doc_format.start_list("letter"))
        self.in_sublist = True

    # Ends a block of path-exclusive lines.
    def end_path_exclusive_lines(self):
        self.scene_buffer.write(doc_format.end_list())
        self.in_sublist = False
