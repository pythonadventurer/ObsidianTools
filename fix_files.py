from config import *
from obsidian import *

inbox = Path(vault,"Inbox")



for note in inbox.iterdir():
    if note.suffix == ".md":
        current_note = ObsidianNote(note)
        current_note.add_file_id()

# # my_note.remove_title()
# my_note.add_file_id()
# # my_note.extract_tags()


