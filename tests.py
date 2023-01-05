from pysidian import *
from pathlib import Path
from tools import *
from config import *

# timestamp tools
print(meta_timestamp())
print(file_timestamp())

# read and write a blank note
my_note = Note()
my_note.metadata["tags"] = ["Testing one two three"]
my_note.metadata["tags"].append("Kitties")
my_note.content = "This is a test of the Emergency Note System."
my_note.write_note()
