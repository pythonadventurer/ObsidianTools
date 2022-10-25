from pathlib import Path
from obsidian import *

folder = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Projects\2020")

for file in folder.iterdir():
    note = ObsidianNote(file)
    note.replace_text("Specimen_#_Field1","Specimen # Field1")
    
    # note.add_file_id()    
    # note.remove_heading(1)
    # note.remove_metadata_key("tags")
    # note.add_metadata("tags", "Projects/2022")   
    # note.remove_line("//Updated:")
    # note.remove_line("//Created")
    # note.remove_line("Created")
    print(f"Processed file: {file.name}")
