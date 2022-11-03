from pathlib import Path
from obsidian import *

folder = Path(r"D:\Rob\Vault\Exercise_Log")

def fix_log(folder_name):
    for item in folder_name.iterdir():
        if item.is_file():
            if item.suffix == ".md":
                note = ObsidianNote(item)

            # note.add_file_id()    
            # note.convert_tags_line()

            # note.remove_heading(1)
            # # # # note.remove_metadata_key("tags")
            # # # # note.add_metadata("tags", "Projects/2022")   
            # # # # note.remove_line("//Updated:")
            # # # # note.remove_line("//Created")
            note.remove_line("Created")
            note.replace_text("./","")

            print(f"Processed file: {item.name}")
        else:
            if item.is_dir():
                fix_log(item)

fix_log(folder)
