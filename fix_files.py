from config import *
from obsidian import *

inbox = Path(vault,"Vault_Inbox")



for note in inbox.iterdir():
    if note.suffix == ".md":
        current_note = ObsidianNote(note)
        current_note.add_file_id()
        current_note.add_tag("Abortion")

        
        # print(current_    note.meta_list)


# # my_note.remove_title()
# my_note.add_file_id()
# # my_note.extract_tags()


