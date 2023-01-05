from pysidian import *
from pathlib import Path
from tools import *
from config import *


print(meta_timestamp())
print(file_timestamp())
new_note = Note()
print(new_note.vault)
# backup(new_note.vault,Path.cwd().parent)
new_note.read_note("test_note.md")
print(new_note.metadata)
print(new_note.content)
print(new_note.filename)
new_note.metadata["inspiration"] = "Dog Tales"
new_note.content = new_note.content.replace("Lorem","Bacon")
new_note.filename = "test_note_2.md"
new_note.write_note()

