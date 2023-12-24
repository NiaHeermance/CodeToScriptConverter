import sys

def bold(text: str) -> str:
	return f'\\textbf{{{text}}}'

def italics(text: str) -> str:
	return f'\\textit{{{text}}}'

def underline(text: str) -> str:
		return f'\\underline{{{text}}}'

def quote(text: str) -> str:
		return f"``{text}''"

def list_item(text: str) -> str:
	return f'\\item {text}\n'

def start_list(bullet_type: str) -> str:
	return f'\\begin{{enumerate}}[{bullet_type}]\n'

def end_list() -> str:
	return "\\end{enumerate}\n"

def get_text_with_style(text: str, style: str) -> str:
	"""
	Given a style ("bold", "underline", "italics", and "quote"), returns provided text in
	said style.

	text -- The text we want to format.
	style -- The style for the text, see above list.
	"""
	if style == "normal":
		return text
	thismodule = sys.modules[__name__]
	style_func = getattr(thismodule, style)
	return style_func(text)

def document_format_start():
	with open("../Code/latex_preamble.txt", "r") as preamble:
		return preamble.read()

def document_format_end():
	return "\\end{document}"