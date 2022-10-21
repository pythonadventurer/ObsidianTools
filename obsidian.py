
from pathlib import Path
from config import *
from datetime import datetime as dt
import os


"""
file does not exist: create new file and assign it a file id in metadata.
file exists:
    - has metadata
        - read into a list
    - does not have metadata
        - add metadata with file id.

Note blocks:
    self.all_text : the entire text contents of the note
    self.metadata_text : the metadata block at the top
    self.body_text : the body of the text that comes after self.metadata_text



Refactor:
- self.read_metadata : read metadata from the file into a list format
- self.write_metadata : create metadata text block from the list
- self.write_file : write the contents of self.metadata and self.body_text to the file
- self.add_file_id : add a file id based on creation date
    - If no existing metadata, create it.
    - If existing metadata, append.

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
 
                # create the metadata list
                self.metadata = [["file_id",[self.file_id]]]
                
                # body text is blank for new notes
                self.body_text = ""

                new_note.write(self.write_metadata(self.metadata))

        else:
            with open(file_path,"r",encoding="utf-8") as new_note:
                self.all_text = new_note.read()

            ctime = os.path.getctime(file_path)
            self.file_id = dt.fromtimestamp(ctime).strftime("%Y.%m.%d.%H.%M.%S.%f")[:23]  
            
            # if the file has no metadata, add file id.
            if self.all_text.startswith("---") == False:    
                self.metadata = [["file_id",[self.file_id]]]
                 
                # since the existing text has no metadata block, body_text = all_text.
                self.write_file(self.write_metadata(self.metadata),self.all_text)
                

            else:
                self.metadata = self.read_metadata(self.all_text)
                self.body_text = self.all_text[len(self.metadata_text):]
                

    def read_metadata(self,text):
        """
        read metadata from text into a list.
        """
        metadata_start = text.find("---\n") + 4
        metadata_end = text.find("---\n",metadata_start)
        metadata_contents = text[metadata_start:metadata_end].split("\n")[:-1]
        for line in range(len(metadata_contents)):
            metadata_contents[line] = metadata_contents[line].split(": ")
            metadata_contents[line][1] = metadata_contents[line][1].split(" ")

        return metadata_contents
   
    def write_metadata(self, metadata):
        """
        User makes changes to the metadata by altering the metadata list.  This list is then
        written to the metadata text.

        Writing the metadata from the list overwrites the existing metadata text.
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


    def add_metadata(self, metadata, key, value):
        """
        If key exists, append the value to its list.
        If key does not exist, add it and the value.
        """
        key_exists = False
        for n in range(len(metadata)):
            if metadata[n][0] == key:
                key_exists = True
                metadata[n][1].append(value)
    
        if key_exists == False:
            if type(value) == list:
                metadata.append([key, value])
            else:
                metadata.append([key,[value]])

        return metadata


    def remove_metadata(self, metadata, key, value):
        # return metadata unchanged if key doesn't exist.
        for n in range(len(metadata)):
            if metadata[n][0] == key:  
                if type(metadata[n][1]) == list:
                    metadata[n][1].remove(value)
                else:
                    metadata[n][1] = metadata[n][1].replace(value + " ","")

            return metadata


    def remove_key(self, metadata, key):
        for n in range(len(metadata)):
            if metadata[n][0] == key:
                metadata.remove(metadata[n])
                return metadata


    def remove_heading(self, level, text):
        """
        Remove the first heading encountered in the text that corresponds to the selected level.
        """
        heading_text = "#" * level + " "
        heading = text[text.find(heading_text):text.find("\n",text.find(heading_text))]
        text = text.replace(heading + "\n", "")
        return text

    def add_heading(self, level, heading_text, text):
        heading_text = "#" * level + " " + heading_text
        text = text + heading_text + "\n"
        return text


    def add_paragraph(self, paragraph, text):
        """
        Add a paragraph to the text and return the text.
        """
        text = text + paragraph + "\n\n"
        return text

    def add_bullet_list(self, list, text):
        for item in list:
            text += "- " + item + "\n"
        text += "\n"
        return text

    def remove_line(self,start_text, text):
        """
        Remove a line within the text that starts with start_text.
        Return the text of the removed line.
        """
        for line in text.split("\n"):
            if line.startswith(start_text):
                line_text = line
        
        text = text.replace(line_text + "\n","")
        return text, line_text


    def convert_tags_line(self, metadata, text):
        """
        Converts tags from a line in the text of the note
        to tags in metadata. Overwrites existing tags in
        metadata.
        """
        output = self.remove_line("Tags: ",text)
        
        new_text = output[0]
        tags_line = output[1]
        tags_line = tags_line.replace("Tags: ","")
        tags_line = tags_line.replace("#","")
        tags_line = tags_line.split(" ")
        return add_metadata("tags", tags_line)
        
    def write_file(self,metadata_text,body_text):
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write(metadata_text)
            f.write(body_text)

            


