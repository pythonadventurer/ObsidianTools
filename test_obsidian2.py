from pathlib import Path
from obsidian2 import *

new_note = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\test_note.md")

my_note = ObsidianNote(new_note)

my_note.add_heading("Here is a Bullet List",2)

my_note.add_bullet_list(["Tracer","Sniper","Pistol","Shotgun","Airsoft"])



my_note.remove_key("tags")
# # my_note.add_metadata("file_id",my_note.file_id)


# my_note.add_metadata("tags","ice_cream")

# # my_note.remove_metadata("tags", "my_stuff")

# # my_note.remove_heading(1)

