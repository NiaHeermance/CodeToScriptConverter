import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Code.renpy_reader import RenpyReader

renRead = RenpyReader("../Tests/TestInput/matching_test.txt")

match = renRead._RenpyReader__isTagMatch("the cat", 0, "the cat\nis very\ncool.")
print(match.file_index, match.line_index)

match = renRead._RenpyReader__isTagMatch("the cat", 0, "the ")
print(match.file_index, match.line_index)
