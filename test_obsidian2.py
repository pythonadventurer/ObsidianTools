from pathlib import Path
from obsidian import *

new_note = Path(vault,"Vault_Inbox/Test Note.md")
if new_note.exists():
    new_note.unlink()

my_note = ObsidianNote(new_note)
my_note.add_file_id()
my_note.add_metadata("tags",["Pizza","Ice_Cream","Kitties"])
my_note.add_heading(1, "A Note About Nice Things")
my_note.add_paragraph("Pizza, ice cream and kitties are very nice.")
my_note.add_paragraph("Other things are nice also, but I don't feel like writing about them.")
my_note.add_heading(2, "List of Nice Kitties")
my_note.add_bullet_list(["Brandy","Ripley","Dashie","Tita"])
my_note.add_heading(2, "List of Yummy Ice Cream Flavors")
my_note.add_bullet_list(["Strawberry","Chocolate","Maple Walnut"])
my_note.add_heading(2, "List of Delicious Types of Pizza")
my_note.add_bullet_list(["Pepperoni","Veggie","Cheese","Meat"])
my_note.remove_heading(1)




