
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# script_instruction.py
# Nia~
#
# A class that represents the end of a script file or the start of a new scene.
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

class ScriptInstruction:
	pass


class NewScene(ScriptInstruction):
	"""
	A script instruction that is used to communicate to start a new scene.
	"""
	def __init__(self, sceneName: str):
		self.sceneName = sceneName


class EndDocument(ScriptInstruction):
	"""
	A script instruction that is used to communicate that a script file should end.
	"""
	pass