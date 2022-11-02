from config import *
import pypandoc
from pathlib import Path

input_file = Path(vault,r"Databases\DataManager2\User Documentation\Main Switchboard.md")
output_file = Path(vault,r"Databases\DataManager2\User Documentation\Main_Switchboard.html")


output = pypandoc.convert_file(input_file, "html",outputfile=output_file)

