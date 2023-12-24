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
		self.output_file = open(f'../Output/{file_name}.txt', "w")


	def write_line(self, character, text, style):
		line = f'{character}: {get_text_with_style(text, style)}'
		self.scene_buffer.write(list_item(line))

		self.scene_characters.add(character)


	def pathExclusiveLine(self, character, text, style):
		self.scene_buffer.write(start_list("a."))

		self.write_line(character, text, style)
		self.in_sublist = True


	def pathAlternateLine(self, character, text, style):
		if not self.in_sublist:
			self.scene_buffer.write(list_item(""))
			self.in_sublist = True

		self.pathExclusiveText(character, text, style)


	def addLine(self, character, text, style):
		if self.in_sublist:
			self.scene_buffer.write(end_list())
			self.in_sublist = False

		self.write_line(character, text, style)


	def writeCharacterList(self, io_buffer, characters):
		io_buffer.write("Characters: ")
		for i, character in enumerate(characters):
			if i != len(characters)-1:
				io_buffer.write(f'{character},')
			else:
				io_buffer.write(f'{character}\n\n')


	def beginDocument(self, name):
		self.output_file.write(document_format_start())
		self.output_file.write(f'{name}\n')


	def beginScene(scene_name):
		self.scene_buffer = StringIO()
		self.scene_characters.clear()

		text = bold(f'Scene {self.scene_count}, {scene_name}')
		self.scene_count += 1
		self.document_buffer.write(f'\n\n\n{text}\n')
		
		self.scene_buffer.write(start_list("1."))


	def finishScene(self):
		self.scene_buffer(end_list())

		self.writeCharacterList(self, self.document_buffer, self.scene_characters)
		self.document_buffer.write(self.scene_buffer.read())

		self.document_characters.update(self.scene_characters)
		self.scene_buffer.close()


	def endDocument(self):
		self.writeCharacterList(self, self.output_file, self.document_characters)
		self.output_file.write(self.document_buffer.read())
		self.output_file.write(document_format_end())
