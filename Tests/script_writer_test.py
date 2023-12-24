import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Code')))

from script_writer import ScriptWriter

sw = ScriptWriter("apple")
sw.beginDocument("A Good Place")
sw.beginScene("Time to dance!")
sw.addLine("Jess", "Well, I'm not sure about prefer exactly.", "italics")
sw.addLine("Jess", "Okay, sure.", "normal")
sw.addLine("Emily", "How are you doing?", "bold")
sw.endScene()
sw.beginScene("Another event")
sw.addLine("Sylvia", "Yo.", "underline")
sw.addLine("Margaret", "Hiiiiii", "quote")
sw.endScene()
sw.endDocument()
