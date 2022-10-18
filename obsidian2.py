# Obisidian 2

from pathlib import Path
from config import *
from datetime import datetime as dt
import os


"""
[["file_id","2022.10.16.15.58.07.556"],
 ["tags",["Politics","Christianity"]],
 ["]

"""

class ObsidianNote:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        if file_path.suffix != ".md":
            print("Can't create note -- invalid file. Must have extension *.md")
            return None

        elif self.file_path.exists() == False:
            with open(file_path,"w",encoding="utf-8") as new_note:
                ctime = os.path.getctime(file_path)
                self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
                self.metadata = f"---\nfile_id: {self.file_id}\n---\n"
                new_note.write(self.metadata)
                self.text = ""

    
    

