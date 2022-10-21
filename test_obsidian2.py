from pathlib import Path
from obsidian2 import *

new_note = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\test_note.md")

my_note = ObsidianNote(new_note)

# my_note.add_heading("Ice Cream List", 2)
# my_note.add_bullet_list(["Vanilla","Rocky Road","Strawberry"])
# my_note.add_heading("Pizza List", 2)
# my_note.add_bullet_list(["Plain Cheese","Pepperoni","Anchovy","Sausage"])

# my_note.convert_tags_line()

my_note.remove_metadata("tags", "Pizza")


