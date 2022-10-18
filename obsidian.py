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
        try:
            with open(self.file_path,"r") as f:
                self.text = f.read()
        except UnicodeDecodeError:
            with open(self.file_path,"r",encoding="utf-8") as f:
                self.text = f.read()

        ctime = os.path.getctime(file_path)
        self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
        self.meta_list = []
        if self.text.startswith("---"):
            self.metadata = self.text[3:self.text.find("---",3)]
            for line in self.metadata.split("\n"):
                if ": " in line:
                    line = line.split(": ")
                    self.meta_list.append([line[0], line[1]])

            for item in self.meta_list:
                if item[0] == "tags":
                    item[1] = [tag for tag in item[1].split(" ")]

        else:
            self.metadata = None

    def save_text(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write(self.text)

    def update_metadata(self):
        if self.meta_list != []:
            new_metadata = "\n"
            for item in self.meta_list:
                if item[0] == "tags":
                    if len(item[1]) > 1:
                        tags_string = " ".join(item[1])
                    else:
                        tags_string = item[1][0]

                    new_metadata += "tags: " + tags_string + "\n"
                else:
                    new_metadata += item[0] + ": " + item[1] + "\n"

            if self.metadata == None:
                self.text = "---" + new_metadata + "---\n" + self.text

            else:
                self.text = self.text.replace(self.metadata, new_metadata)

            self.save_text()

    def extract_tags(self):
        has_tags = False
        for item in meta_list:
            if item[0] == "tags":
                has_tags = True

        if "Tags: " in self.text and has_tags == False:
            tags_line = self.text[self.text.find("Tags: "):self.text.find("\n",self.text.find("Tags: "))].strip()
            tags_string = self.text[self.text.find("Tags: ") + 6:self.text.find("\n",self.text.find("Tags: ") + 6)]
            tags_string = tags_string.strip()
            if " " not in tags_string:
                self.meta_list.append(["tags", [tags_string.replace("#","")]])

            else:    
                self.meta_list.append(["tags",[tag.replace("#","") for tag in tags_string.split(" ")]])

            self.text = self.text.replace(tags_line + "\n","")
            self.update_metadata()

    def add_file_id(self):
        has_id = False
        for item in self.meta_list:
            if item[0] == "file_id":
                has_id = True
        if has_id == False:
            self.meta_list.append(["file_id",self.file_id])
            self.update_metadata()

        # remove created date if exists
        if "Created: " in self.text:
            created_line = self.text[self.text.find("Created: "):self.text.find("\n",self.text.find("Created: "))]
            self.text = self.text.replace(created_line,"")
            self.save_text()

    def add_tag(self, tag):
        has_tags = False
        for item in self.meta_list:
            if item[0] == "tags":
                has_tags == True
        
        if has_tags == True:
            for item in self.meta_list:
                if item[0] == "tags":
                    item[1].append(tag)

        else:
            self.meta_list.append(["tags",[tag]])

        self.update_metadata()
    
    def remove_tag(self,tag):
        if "tags" in self.meta_list:
            for item in self.meta_list:
                if item[0] == "tags":
                    if tag in item[1]:
                        item[1].remove(tag)


        
    def list_tags(self):
        for tag in self.meta_dict["tags"]:
            print(tag)

    def remove_title(self):
        if self.text.find("# ") != -1:
            self.title = self.text[self.text.find("# "):self.text.find("\n",self.text.find("# "))]
            self.text = self.text.replace(self.title + "\n","")
            self.save_text()








