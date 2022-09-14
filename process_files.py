from config import *
from lib import *
from pathlib import Path

target_dir = Path(r"D:\Rob\Vault\03 Notes")

for item in target_dir.iterdir():
    if item.is_file():
        new_file = ObsidianNote(item)
        new_file.tags_to_content()
        print(item.name)
        
































