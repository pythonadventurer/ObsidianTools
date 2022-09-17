from config import *
from lib import *
from pathlib import Path

def review_files(target_dir):
    """
    Every Markdown file in the vault.
    """
    for item in Path(target_dir).iterdir():
        if item.is_file() and item.suffix == ".md":
            new_file = ObsidianNote(item)
            print(item.name)
            if "Git" in new_file.tags and "Templates" not in str(item.parent):
                pass
                # new_file.tags.remove("Git")
                # new_file.tags.append("Coding_and_Development/Git")
                # new_file.write_file()
                
        elif item.is_dir():
            review_files(item)    


review_files(vault)







































