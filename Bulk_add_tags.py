from config import *
from lib import *

for file in resource_catalog.iterdir():
    try:
        note = ObsidianNote(file)
        if note.metadata["tags"] == []:
            print("Tagging: " + file.name)
            note.add_tag("Exercise_Log_Resources")
            note.save()
    except UnicodeDecodeError:
        continue



