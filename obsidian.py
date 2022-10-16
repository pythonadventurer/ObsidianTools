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
        self.meta_dict = {}
        if self.text.startswith("---"):
            self.metadata = self.text[3:self.text.find("---",3)]
            for line in self.metadata.split("\n"):
                if ": " in line:
                    line = line.split(": ")
                    self.meta_dict[line[0]] = line[1]
            if "tags" in self.meta_dict.keys():
                self.meta_dict["tags"] = [tag for tag in self.meta_dict["tags"].split(" ")]

        else:
            self.metadata = None

    def save_text(self):
        with open(self.file_path,"w") as f:
            f.write(self.text)

    def update_metadata(self):
        if self.meta_dict != {}:
            new_metadata = "\n"
            for key in self.meta_dict.keys():
                if key == "tags":
                    if len(self.meta_dict["tags"]) > 1:
                        tags_string = " ".join(self.meta_dict["tags"])
                    else:
                        tags_string = self.meta_dict["tags"][0]

                    new_metadata += "tags: " + tags_string + "\n"
                else:
                    new_metadata += key + ": " + self.meta_dict[key] + "\n"
            if self.metadata == None:
                self.text = "---" + new_metadata + "---\n" + self.text

            else:
                self.text = self.text.replace(self.metadata, new_metadata)

            self.save_text()

    def extract_tags(self):
        if "Tags: " in self.text and "tags" not in self.meta_dict.keys():
            tags_line = self.text[self.text.find("Tags: "):self.text.find("\n",self.text.find("Tags: "))].strip()
            tags_string = self.text[self.text.find("Tags: ") + 6:self.text.find("\n",self.text.find("Tags: ") + 6)]
            tags_string = tags_string.strip()
            if " " not in tags_string:
                self.meta_dict["tags"] = [tags_string.replace("#","")]

            else:    
                self.meta_dict["tags"] = [tag.replace("#","") for tag in tags_string.split(" ")]
            self.text = self.text.replace(tags_line + "\n","")
            self.update_metadata()

    def add_file_id(self):
        self.meta_dict["file_id"] = self.file_id
        self.update_metadata()

        if "Created: " in self.text:
            created_line = self.text[self.text.find("Created: "):self.text.find("\n",self.text.find("Created: "))]
            self.text = self.text.replace(created_line,"")
            self.save_text()

    def add_tag(self, tag):
        self.meta_dict["tags"].append(tag)
        self.update_metadata()
    
    def remove_tag(self,tag):
        try:
            self.meta_dict["tags"].remove(tag)
            self.update_metadata()
        except ValueError:
            print(f"Sorry, tag {tag} not found.")
        
    def list_tags(self):
        for tag in self.meta_dict["tags"]:
            print(tag)

    def remove_title(self):
        if self.text.find("# ") != -1:
            self.title = self.text[self.text.find("# "):self.text.find("\n",self.text.find("# "))]
            self.text = self.text.replace(self.title + "\n","")
            self.save_text()








