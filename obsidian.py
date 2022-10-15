from pathlib import Path
from config import *
from datetime import datetime as dt
import os

# test_file = Path(vault,"Notes/Highway to Hell.md")
test_file = Path(vault, "Notes/Mike’s Midterm Tsunami Truth 5 - Michael Moore.md")
# ctime = os.path.getctime(test_file)

# print(dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f"))

# timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:19]

# print(timestamp)


class ObsidianNote:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        try:
            with open(self.file_path,"r") as f:
                self.text = f.read()
        except UnicodeDecodeError:
            with open(self.file_path,"r",encoding="utf-8") as f:
                self.text = f.read()

        ctime = os.path.getctime(test_file)
        self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
        self.meta_dict = {}
        if self.text.startswith("---"):
            self.metadata = self.text[3:self.text.find("---",3)]
            for line in self.metadata.split("\n"):
                if line != "" and ": " in line:
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
        new_metadata = "\n"
        for key in self.meta_dict.keys():
            if key == "tags":
                tags_string = " ".join(self.meta_dict["tags"])
                new_metadata += "tags: " + tags_string + "\n"
            else:
                new_metadata += key + ": " + self.meta_dict[key] + "\n"
        if self.metadata == None:
            self.text = "---" + new_metadata + "---\n" + self.text

        else:
            self.text = self.text.replace(self.metadata, new_metadata)

        self.save_text()

    def extract_tags(self):
        if "Tags: " in self.text:
            tags_line = self.text[self.text.find("Tags: "):self.text.find("\n",self.text.find("Tags: "))]
            tags_string = self.text[self.text.find("Tags: ") + 6:self.text.find("\n",self.text.find("Tags ") + 6)]
            self.meta_dict["tags"] = [tag.replace("#","") for tag in tags_string.split(" ")]
            self.text = self.text.replace(tags_line,"")
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


my_note = ObsidianNote(test_file)










