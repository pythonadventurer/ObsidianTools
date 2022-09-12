import config
from lib import *

def list_files(folder):    
    for obj in folder.iterdir():
        if obj.is_file():
            if obj.suffix == ".md":
                curr_obj = ObsidianNote(obj)
                if curr_obj.get_frontmatter() == None:
                    print(curr_obj.name)


        else:
            list_files(obj)



list_files(config.vault) 

















