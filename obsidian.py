
from pathlib import Path
from config import *
from datetime import datetime as dt
import os


"""

"""

class ObsidianNote:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        if file_path.suffix != ".md":
            print("Invalid file. Must have extension *.md")
            return None

        elif self.file_path.exists() == False:
            # All new notes get a file ID based on the creation time.
            with open(file_path,"w",encoding="utf-8") as new_note:
                ctime = os.path.getctime(file_path)
                self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
 
        else:
            with open(file_path,"r",encoding="utf-8") as new_note:
                ctime = os.path.getctime(file_path)
                self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]
                self.all_text = new_note.read()

            self.metadata = self.read_metadata()
            if self.metadata != []:
                self.body_text = self.all_text[len(self.write_metadata(self.metadata)):]

            else:
                self.body_text = self.all_text
                

    def read_metadata(self):
        """
        read metadata from text into a list.
        """
        if self.all_text.find("---\n") == -1:
            return []

        else:
            metadata_start = self.all_text.find("---\n") + 4
            metadata_end = self.all_text.find("---\n",metadata_start)
            metadata_contents = self.all_text[metadata_start:metadata_end].split("\n")[:-1]
            for line in range(len(metadata_contents)):
                metadata_contents[line] = metadata_contents[line].split(": ")
                metadata_contents[line][1] = metadata_contents[line][1].split(" ")

            return metadata_contents
   
    def write_metadata(self, metadata):
        """
        User makes changes to the metadata by altering the metadata list.  This list is then written to the metadata text.

        """
        new_metadata = "---\n"

        for line in range(len(metadata)):
            new_metadata += metadata[line][0] + ": "
            if len(metadata[line][1]) > 1:
                new_metadata += " ".join(metadata[line][1]) + "\n"
            else:
                new_metadata += metadata[line][1][0] + "\n"

        new_metadata += "---\n"    

        return new_metadata


    def add_metadata(self, key, value):
        """
        If key exists, append the value to its list.
        If key does not exist, add it and the value.
        """
        key_exists = False
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:
                key_exists = True
                if type(value) == list:
                    self.metadata[n][1].extend(value)
                else: 
                    self.metadata[n][1].append(value)
    
        if key_exists == False:
            if type(value) == list:
                self.metadata.append([key, value])
            else:
                self.metadata.append([key,[value]])
            
        self.save_file()


    def add_file_id(self):
        self.add_metadata("file_id",self.file_id)


    def remove_metadata_value(self, key,value):
        # remove the selected value from a metadata item
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:  
               self.metadata[n][1].remove(value)
               self.save_file()

    def remove_metadata_key(self, key):
        for n in range(len(self.metadata)):
            if self.metadata[n][0] == key:
                self.metadata.remove(self.metadata[n])
                self.save_file()

    def convert_tags_line(self):
        """
        Converts tags from a line in the text of the note
        to tags in metadata. Overwrites any existing tags in
        metadata.
        """
        for line in self.body_text.split("\n"):
            if line.startswith("Tags: "):
                tags_line = line
                new_tags_line = tags_line.replace("Tags: ","")
                new_tags_line = new_tags_line.replace("#","")
                # all that's left now is tags separated by spaces.
                new_tags_line = new_tags_line.split(" ")
                self.remove_metadata_key("tags")
                self.add_metadata("tags", new_tags_line)
                self.remove_line("Tags: ")
                self.save_file()


    def remove_heading(self, level):
        """
        Remove the first heading encountered in the text that corresponds to the selected level.
        """
        heading_text = "#" * level + " "
        heading = self.body_text[self.body_text.find(heading_text):self.body_text.find("\n",self.body_text.find(heading_text))]
        if heading != "":
            self.body_text = self.body_text.replace(heading + "\n", "")
            self.save_file()

    def remove_line(self,start_text):
        """
        Remove a line within the text that starts with start_text.
        Return the text of the removed line.
        """
        for line in self.body_text.split("\n"):
            if line.startswith(start_text):
                line_text = line 
                self.body_text = self.body_text.replace(line_text + "\n","")
                self.save_file()

    def add_heading(self, level, heading_text):
        heading_text = "#" * level + " " + heading_text
        self.body_text = self.body_text + heading_text + "\n"
        self.save_file()

    def add_title(self, title_text):
        # Add a level 1 title to the top of the file
        title_text = "# " + title_text + "\n"
        self.body_text = title_text + self.body_text
        self.save_file()      



    # def add_paragraph(self, paragraph, text):
    #     """
    #     Add a paragraph to the text and return the text.
    #     """
    #     text = text + paragraph + "\n\n"
    #     return text

    # def add_bullet_list(self, list, text):
    #     for item in list:
    #         text += "- " + item + "\n"
    #     text += "\n"
    #     return text




 
        
    def save_file(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            if self.metadata != []:
                f.write(self.write_metadata(self.metadata))
            f.write(self.body_text)


            


