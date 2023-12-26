import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Config", "Files"))
)

from filenames_to_document_titles import get_document_title

files = os.listdir("../Input")

for file in files:
    dot = file.rindex(".")
    print(get_document_title(file[:dot]))
