from config import *
from lib import *
from pathlib import Path

for file in Path(r"D:\Rob\Vault_02\Exercise_Log").iterdir():
    if file.suffix == ".md":
        fix_file = ObsidianNote(file)
        # print(fix_file.content)
        print(fix_file.title)
        
        # fix_file.remove_frontmatter()
        # print("Processed: " + file.name)
        











