from PySidian import *
from config import *
from pathlib import Path
from tools import *
# notes_dir = Path(new_vault,"03-Notes")
notes_dir = Path(current_vault,"Notes")
dest_dir = Path(new_vault,"05-Daily-Notes")

for item in notes_dir.iterdir():
	if item.suffix == ".md":
		new_note = Note()
		new_note.read_note(item)
		if "tags" in new_note.metadata.keys():
			if "Journal_Archive/2022" in new_note.metadata["tags"]:
				new_note.filepath = Path(dest_dir,item.name)
				new_note.write_note()
				print("Processed: " + item.name)





