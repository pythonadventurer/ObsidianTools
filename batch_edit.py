from pathlib import Path
from obsidian import *

folder = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Notes")

def fix_log(folder_name):
    for item in folder_name.iterdir():
        if item.is_file():
            if item.suffix == ".md":
                note = ObsidianNote(item)

            # note.add_file_id()    
            # note.convert_tags_line()

            # note.remove_heading(1)
           
            # # # # note.add_metadata("tags", "Projects/2022")   
            # # # # note.remove_line("//Updated:")
            # # # # note.remove_line("//Created")
            # note.remove_line("Created")
            # note.replace_text("./","")
                note.remove_metadata_key("file_id")
                print(f"Processed file: {item.name}")
 

fix_log(folder)
