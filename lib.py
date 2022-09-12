from argparse import MetavarTypeHelpFormatter
from pathlib import Path
import re
import csv
from time import sleep


def convert_zim_header(zim_header):
    '''
    Convert a ZimWiki heading to Markdown.

    ====== 2022-02-14 Replace LogAppend with SendToLog ======

    becomes:

        # 2022-02-14 Replace LogAppend with SendToLog

    ===== SendToLog =====

    becomes:

    ## SendToLog

    '''
    header = re.match("^={2,}",zim_header)
    if header != None:
        if len(header[0]) == 6:
            md_header = "#"
        elif len(header[0]) == 5:
            md_header = "##"
        elif len(header[0]) == 4:
            md_header = "###"
        elif len(header[0]) == 3:
            md_header = "####"
        elif len(header[0]) == 2:
            md_header = "#####"

        new_header = md_header + zim_header.replace("=","")

        return new_header

    else:
        return None

def zim_to_md(zim_file,dest_dir):
    with open(zim_file,"r",encoding='utf-8') as f:
        content = f.read().split("\n")
    
    new_content = []

    for line in content:
    
        # Exclude lines with ZimWiki headings
        if "Page ID" not in line[:10] \
            and "Content-Type:" not in line \
            and "Wiki-Format:" not in line \
            and "Creation-Date:" not in line:

            if re.match("^={2,}",line) != None:
                new_line = convert_zim_header(line)
            
            else:
                # Convert check boxes and bullet points
                if "[*] " in line:
                    new_line = line.replace("[*] ","- [x] ")

                elif "[ ] " in line:
                    new_line = line.replace("[ ] ","- [ ] ")

                elif "* " in line:    
                    new_line = line.replace("* ","- ")

                else:
                    new_line = line

            new_content.append(new_line)

    new_content = "\n".join(new_content)
    new_file_path = Path(dest_dir,zim_file.stem + ".md")
    with open(new_file_path,"w",encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Created file: {new_file_name}")

def remove_file_ids(folder):
    '''
    Remove all file IDs from files.
    '''
    for item in folder.iterdir():
        new_name = Path(folder,item.name[9:].replace("_"," "))
        item.rename(new_name)
        print(new_name)

def resource_files_list(resource_folder,target_file):
    resource_list = [[file.name, str(file)] for file in Path(resource_folder).iterdir()]
    with open(target_file,"w",newline="",encoding="utf-8") as f:
        list_writer = csv.writer(f)
        list_writer.writerows(resource_list)

class ObsidianNote:
    """
    Read, create and edit Obisidian notes.
    """
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.text = self.read_file(self.file_path)
        self.frontmatter = self.get_frontmatter()
        self.metadata = self.get_metadata()
        self.title = self.get_title()
        self.content = self.get_content()
 
        # self.links = self.get_links()

    def read_file(self,file_path):
        """
        Read the selected file_name in NotesFolder
        """
        try:
            with open(file_path,"r") as f:
                return f.read()

        except UnicodeDecodeError:
            with open(file_path,"r",encoding="utf-8") as f:
                return f.read()
                

    def update_text(self):
        """
        Update the text with any changes made.
        """
        self.frontmatter = self.update_frontmatter()
        if "# " not in self.title:
            self.title = "# " + self.title
        new_text = self.frontmatter + self.title + self.content
        return new_text


    def save(self):
        """
        Write out the file
        """
        self.text = self.update_text()
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write(self.text)

    def get_frontmatter(self):
        """
        Frontmatter string
        """
        try:
            frontmatter_start = self.text.find("---")
            frontmatter_end = self.text.find("---",frontmatter_start + 1)
            frontmatter =  self.text[frontmatter_start:frontmatter_end + 3]
        except IndexError:
            frontmatter = None

        return frontmatter

    def get_metadata(self):
        """
        Metadata dict from frontmatter
        """
        metadata_dict = {}
        if self.frontmatter != None:
            frontmatter = self.text.split("---")[1]
            frontmatter = frontmatter.split("\n")

            for item in frontmatter:
                if item != '':
                    if "created: " in item:
                        metadata_dict["created"] = item[8:].strip()
                    else:
                        new_item = item.split(":")
                        metadata_dict[new_item[0]] = new_item[1].strip()
            
            tags = metadata_dict["tags"][1:len(metadata_dict["tags"])-1].split(",")
            tags = [tag.strip() for tag in tags]
            if '' in tags:
                tags.remove('')

            metadata_dict["tags"] = tags
            return metadata_dict
        else:
            return None

    def update_frontmatter(self):
        """
        Update the frontmatter string from the dict
        """
        if self.metadata != None:
            new_frontmatter = "---\n"
            for key in self.metadata.keys():
                new_frontmatter += key + ": "
                if key.upper() == "TAGS":
                    new_frontmatter += str(self.metadata[key]).replace("'","") + "\n"
                else:     
                    new_frontmatter += self.metadata[key] + "\n"
            new_frontmatter += "---\n"
            return new_frontmatter
        else:
            print("File has no frontmatter.")

    def get_content(self):
        """
        content except metadata and title, if present
        """
        title = self.get_title()
        if title == "":
            return self.text[len(self.frontmatter):]
        else:
            return self.text[len(self.frontmatter) + len(title)+3:]

    def get_title(self):
        """
        Title of the file. Must be first line of content and start with "# ".
        """
        title = self.text[len(self.frontmatter)+1:]
        if title[:2] == "# ":
            title = self.text[self.text.find("# "):self.text.find("\n",self.text.find("# ")+1)].replace("# ","")
        else:
            title = ""
        
        return title

    def get_links(self):
        """
        List of links in the note content
        """
        links = []
        for line in self.text.split("\n"):
            match = re.match("!\[\[.+\]\]|\[\[.+\]\]",line)
            if match != None:
                links.append(match[0])
        return links

    def add_tag(self,tag_name):
        self.metadata["tags"].append(tag_name)
        self.text = self.update_text()

    def remove_tag(self,tag_name):
        try:
            self.metadata["tags"].remove(tag_name)
            self.text = self.update_text()
        except ValueError:
            print(f"Tag: '{tag_name} does not exist.")

    def delete_tags(self):
        self.metadata["tags"] = []
        self.text = self.update_text()

    def set_title(self,title_text):
        self.title = "# " + title_text


class ObsidianResource:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.metadata_file = self.get_metadata_file()

    def move_to_vault(self,vault_path):
        pass

    def get_metadata_file(self):
        return "INFO_" + self.file_path.stem + "_" + \
            self.file_path.suffix[1:].upper()

    
    
    