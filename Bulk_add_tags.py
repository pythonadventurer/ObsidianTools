from config import *
from lib import *

for file in resource_catalog.iterdir():
    try:
        note = ObsidianNote(file)
        if note.metadata["tags"] == []:
            print("Tagging: " + file.name)
            note.add_tag("Humor/Dilbert")
            note.save()
    except UnicodeDecodeError:
        continue



