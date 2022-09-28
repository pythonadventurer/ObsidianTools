from config import *
from  pathlib import Path



def zim_export(zim_dir):    
    for item in Path(zim_dir).iterdir():
        if item.is_file(): 
            if item.suffix.upper() == ".TXT":
                print(item.name)
        else:
            zim_export(item)



zim_export(zim_dir)



