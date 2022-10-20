from pathlib import Path
from obsidian2 import *

new_note = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\test_note.md")

my_note = ObsidianNote(new_note)

my_note.remove_key("tags")
my_note.add_metadata("tags", "my_stuff")
my_note.add_metadata("tags","ice_cream")


my_note.remove_metadata("tags", "my_stuff")

print(my_note.metadata)

