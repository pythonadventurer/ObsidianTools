from lib import *
from config import *
from pathlib import Path


for file in resource_catalog.iterdir():
    file_obj = ObsidianNote(file)
    if file_obj.title != file.stem:
        file_obj.set_title(file.stem)
        file_obj.save()
        print("Fixed: " + file.name)
            

