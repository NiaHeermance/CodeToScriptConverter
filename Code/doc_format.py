import sys
import os

# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'
#
# doc_format.py
# Nia~
#
# These functions can be used to create simple LaTeX documents with lists and stylized text.
#
# _,.-'~'-.,__,.-'~'-.,__,.-'~'-.,__,.-'~'

def bold(text: str) -> str:
    return f'\\textbf{{{text}}}'

def italics(text: str) -> str:
    return f'\\textit{{{text}}}'

def underline(text: str) -> str:
    return f'\\underline{{{text}}}'

def quote(text: str) -> str:
        return f"``{text}''"

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


def start_list(bullet_type: str) -> str:
    label = "label = "
    if bullet_type == "number":
        label += "\\arabic*."
    elif bullet_type == "letter":
        label += "\\alph*."

    return f'\\begin{{enumerate}}[{label}]\n'

def list_item(text: str) -> str:
    return f'\\item {text}\n'

def end_list() -> str:
    return "\\end{enumerate}\n"

def new_line() -> str:
    return "\\\\"


def document_format_start():
    with open("../Code/latex_preamble.txt", "r") as preamble:
        return preamble.read()

def document_format_end():
    return "\\end{document}"


def renderDocument(file_path: str):
    """
    Given a file_path, renders the tex file into a PDF
    file_path -- absolute or relative path to a .tex file.
    """
    final_slash = file_path.rindex("/")
    output_directory = file_path[:final_slash]
    aux_directory = output_directory + "/AuxiliaryFiles"
    os.system(f'pdflatex {file_path} --output-directory={output_directory} --aux-directory={aux_directory}')
