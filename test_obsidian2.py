from pathlib import Path
from obsidian import *

new_note = Path(vault,"Vault_Inbox/Test Note.md")
existing_note = Path(vault, "Vault_Inbox/Hitler on Christianity and the Nation.md")
old_note = Path(vault, "Vault_Inbox/Choosing the Right Container.md")


my_note = ObsidianNote(new_note)
my_existing_note = ObsidianNote(existing_note)
my_old_note = ObsidianNote(old_note)

# print(my_note.metadata) 
# print(my_existing_note.metadata)
# print(my_existing_note.body_text)

# my_note.add_file_id()

# my_note.add_metadata("tags", ["frogs","snails"])
# my_note.remove_line("This is the barn")

my_old_note.convert_tags_line()






# my_note.remove_metadata_value("tags", "frogs")

# my_note.remove_metadata_key("tags")


