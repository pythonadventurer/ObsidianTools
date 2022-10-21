from pathlib import Path
from obsidian import *

folder = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Changelog\2019")

for file in folder.iterdir():
    note = ObsidianNote(file)
    print(f"Processed file: {file.name}")
