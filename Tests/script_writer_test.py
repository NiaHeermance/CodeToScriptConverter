import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Code.script_writer import ScriptWriter
from Code.dialogue import TextStyle

sw = ScriptWriter("apple")
sw.beginDocument("A Good Place")
sw.beginScene("Time to dance!")
sw.addLine("Jess", "Well, I'm not sure about prefer exactly.", TextStyle.ITALICS)
sw.addLine("Jess", r"Okay, {i}sure{\i}.", TextStyle.NORMAL)
sw.addPathExclusiveLine("Bell", "Hiii!", TextStyle.NORMAL, reason = "Yooo")
sw.addPathExclusiveLine("Bell", "I'm pretty cool.", TextStyle.BOLD)
sw.addLine("Emily", "How are you doing?", TextStyle.BOLD)
sw.endScene()
sw.beginScene("Another event")
sw.addLine("Amelia", "Yo.", TextStyle.UNDERLINE)
sw.addLine("Jess", "Hiiiiii", TextStyle.QUOTE)
sw.addPathExclusiveLine("Amelia", "What's up?", TextStyle.NORMAL, reason = "dog")
sw.addPathExclusiveLine("Jess", "Nothing much.", TextStyle.NORMAL)
sw.addPathExclusiveLine("Jess", "I love you!", TextStyle.BOLD, reason = "NEW")
sw.addPathExclusiveLine("Amelia", r"Me too. {q}Testing weird {b}stuff{\b}{\q}", TextStyle.NORMAL)
sw.endScene()
sw.endDocument()
sw.renderDocument()
