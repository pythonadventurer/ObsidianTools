from PySidian import *
from config import *
from pathlib import Path
from tools import *
notes_dir = Path(current_vault,"Notes")
for item in notes_dir.iterdir():
	if item.suffix == ".md":
		# print("Processing: " + item.name)
		new_note = Note()
		new_note.read_note(item)
		new_note.content = fix_task_icons(new_note.content)
		new_note.content.replace("#task","#project")
		if "tags" in new_note.metadata.keys():
			if "Projects/2022" in new_note.metadata["tags"]:
				print(item.name)
				new_note.filepath = Path(new_vault, "temp", item.name)
				new_note.write_note()

