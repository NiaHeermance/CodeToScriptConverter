
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# dialogue.py
# Nia~
#
# An object that represents a dialogue line with a character attatched and text styling
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

from enum import Enum

class TextStyle(Enum):
	"""
	An enum representing how a text is stylized.
	"""
	NORMAL = 0
	BOLD = 1
	ITALICS = 2
	UNDERLINE = 3
	QUOTE = 4


class Dialogue:
	"""
	Represents a line in a script. Used as an API to communicate between the RenpyReader and the ScriptWriter
	Note that path_reason should only be non-empty if path_exclusive is True and this is the first line of an
	exclusive lines group.
	"""
	def __init__(self, character: str, line: str, style: TextStyle, path_exclusive: bool = False, path_reason: str = ""):
		self.character = character
		self.line = line
		self.style = style
		self.path_exclusive = path_exclusive
		self.path_reason = path_reason