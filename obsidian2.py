# Obisidian 2

from pathlib import Path
from config import *
from datetime import datetime as dt
import os


"""
[["file_id","2022.10.16.15.58.07.556"],
 ["tags",["Politics","Christianity"]],
 ["]

- Metadata is to consist of key/value pairs.
- Key and value separated by ": "
- Multi-item values separated by spaces.
---
file_id: 2022.10.16.15.58.07.556
tags: Politics Christianity
category: Notes
---

"""

class ObsidianNote:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        if file_path.suffix != ".md":
            print("Can't create note -- invalid file. Must have extension *.md")
            return None

        elif self.file_path.exists() == False:
            # All new notes get a file ID based on the creation time.
            with open(file_path,"w",encoding="utf-8") as new_note:
                ctime = os.path.getctime(file_path)
                self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
                self.metadata_text = f"---\nfile_id: {self.file_id}\n---\n"
                new_note.write(self.metadata_text)
                self.metadata = self.get_metadata()
                self.text = ""

        else:
            with open(file_path,"r",encoding="utf-8") as new_note:
                self.all_text = new_note.read()

            ctime = os.path.getctime(file_path)
            self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]   
            self.metadata_text = self.all_text[self.all_text.find("---")+3:self.all_text.find("---",self.all_text.find("---")+3)]
            self.metadata = self.get_metadata()
            self.text = self.all_text[len(self.metadata_text)+7:]


    def get_metadata(self):
        """
        read the metadata into a list
        """   
        meta_lines = self.metadata_text.split("\n")[1:-1]
        new_list = []
        for line in meta_lines:
            new_list.append(line.split(": "))

        for line in range(len(new_list)):
            try:
                if len(new_list[line][1].split(" ")) > 1:
                    new_list[line][1] = new_list[line][1].split(" ")
            except IndexError:
                pass

        return new_list
    

    def write_metadata(self):
        """
        User makes changes to the metadata by altering the metadata list.  This list is then
        written to the metadata text.

        Writing the metadata from the list overwrites the existing metadata text.
        """
        new_metadata = ""
        for line in self.metadata:
            new_metadata += line[0] + ": "
            if type(line[1]) == list:
                new_metadata += " ".join(line[1]) + "\n"
            else:
                new_metadata += line[1] + "\n"

        self.metadata_text = new_metadata
        self.write_file

    def add_metadata(self,key,value):
        """
        If key exists, append the value to its list.
        If key does not exist, add it and the value.
        """
        key_exists = False
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:
                key_exists = True
                if type(self.metadata[n][1]) == list:
                    self.metadata[n][1].append(value)
                else:
                    if ": " in self.metadata[n][0]:
                        space = ""
                    else:
                        space = " "
                    self.metadata[n][1] += space + value
        if key_exists == False:
            self.metadata.append([key, value])

        self.write_metadata()
        self.write_file()

    
    def remove_metadata(self,key,value):
        key_exists = False
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:  
                key_exists = True
                if type(self.metadata[n][1]) == list:
                    self.metadata[n][1].remove(value)
                else:
                    self.metadata[n][1] = self.metadata[n][1].replace(value + " ","")

        if key_exists == False:
            print("Key does not exist.")

        elif key_exists == True:
            self.write_metadata()
            self.write_file()

    def remove_key(self,key):
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:
                self.metadata.remove(self.metadata[n])
                self.write_metadata()
                self.write_file()
    
    def remove_heading(self,level):
        """
        Remove the first heading encountered in the text that corresponds to the selected level.
        """
        heading_text = "#" * level + " "
        heading = self.text[self.text.find(heading_text):self.text.find("\n",self.text.find(heading_text))]
        self.text = self.text.replace(heading + "\n", "")
        self.write_file()

    def add_heading(self,text,level):
        heading_text = "#" * level + " " + text
        self.text = self.text + heading_text + "\n"
        self.write_file()

    def add_paragraph(self,text):
        self.text = self.text + text + "\n\n"
        self.write_file()

    def add_bullet_list(self,list):
        for item in list:
            self.text += "- " + item + "\n"
        self.text += "\n"
        self.write_file()



    def write_file(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write("\n---" + self.metadata_text + "\n---\n")
            f.write(self.text)



