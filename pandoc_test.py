from config import *
import pypandoc
from pathlib import Path
import re

link_search = re.compile("\((.+\.md)\)")
switchboard = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Databases\DataManager2\User Documentation\Main Switchboard.md")

with open(switchboard,"r") as file:
    text = file.read()


# input_dir = Path(vault,r"Databases\DataManager2\User Documentation")
# output_dir = Path(vault,r"Databases\DataManager2\User Documentation\HTML")


# for item in input_dir.iterdir():
#     if item.is_file() and item.suffix == ".md":
#         input_file = Path(input_dir,item.name)
#         output_file = Path(output_dir,item.stem + ".html")
#         title = "--metadata-title=" + input_file.stem.replace("_"," ")

#         output = pypandoc.convert_file(input_file, "html",outputfile=output_file,extra_args=['-s','-c styles/pandoc.css'])
#         print("Converted: " + item.name)

