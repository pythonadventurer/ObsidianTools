from config import *
from obsidian import *

inbox = Path(vault,"Vault_Inbox")



for note in inbox.iterdir():
    if note.suffix == ".md":
        current_note = ObsidianNote(note)
        # current_note.add_file_id()
        # current_note.remove_title()
      #  current_note.extract_tags()

