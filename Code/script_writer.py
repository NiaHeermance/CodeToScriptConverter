from io import StringIO
from doc_format import *

class ScriptWriter:
	def __init__(self, file_name):
		self.in_sublist = False
		
		self.scene_count = 1

		self.scene_characters = set()
		self.document_characters = set()

		self.scene_buffer = StringIO()
		self.document_buffer = StringIO()
		self.output_file = open(f'../Output/{file_name}.tex', "w")


	def writeLine(self, character, text, style):
		line = f'{character}: {get_text_with_style(text, style)}'
		self.scene_buffer.write(list_item(line))

		self.scene_characters.add(character)


	def beginPathExclusiveLines(self):
		if self.in_sublist:
			self.endPathExclusiveLines()

		self.scene_buffer.write(list_item(""))
		self.scene_buffer.write(start_list("a."))
		self.in_sublist = True


	def endPathExclusiveLines(self):
		self.scene_buffer.write(end_list())
		self.in_sublist = False


	def pathExclusiveLine(self, character, text, style):
		if not self.in_sublist:
			self.beginPathExclusiveLines()

		self.writeLine(character, text, style)


	def addLine(self, character, text, style):
		if self.in_sublist:
			self.endPathExclusiveLines()

		self.writeLine(character, text, style)


	def writeCharacterList(self, io_buffer, characters):
		if len(characters) == 0:
			return
		io_buffer.write("Characters: ")
		for i, character in enumerate(characters):
			if i != len(characters)-1:
				io_buffer.write(f'{character}, ')
			else:
				io_buffer.write(f'{character}\n\n')


	def beginDocument(self, name):
		self.output_file.write(document_format_start())
		self.output_file.write(bold(name) + "\n")


	def beginScene(self, scene_name):
		self.scene_buffer = StringIO()
		self.scene_characters.clear()

		text = bold(f'Scene {self.scene_count}, {scene_name}')
		self.scene_count += 1
		self.document_buffer.write(f'\n{text}\n')
		
		self.scene_buffer.write(start_list("1."))


	def endScene(self):
		self.scene_buffer.write(end_list())

		self.writeCharacterList(self.document_buffer, self.scene_characters)
		self.scene_buffer.seek(0)
		self.document_buffer.write(self.scene_buffer.read())
		self.scene_buffer.close()

		self.document_characters.update(self.scene_characters)


	def endDocument(self):
		self.writeCharacterList(self.output_file, self.document_characters)
		self.document_buffer.seek(0)
		self.output_file.write(self.document_buffer.read())
		self.output_file.write(document_format_end())

		self.document_buffer.close()
		self.output_file.close()
