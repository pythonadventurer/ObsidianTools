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


class ObsidianNote:
    def __init__(self,file_path):
        self.file_path = file_path

        # If the file already exists, read its data.
        if file_path.exists():
            try:
                with open(file_path,"r") as f:
                    self.text = f.read()

            except UnicodeDecodeError:
                try:
                    with open(file_path,"r",encoding="utf-8") as f:
                        self.text =  f.read()
                except UnicodeDecodeError:
                    print("File: " + file_path.name + " has thrown a Unicode fit.")
                    
            try:
                frontmatter_start = self.text.find("---")
                frontmatter_end = self.text.find("---",frontmatter_start + 1)
                self.frontmatter =  self.text[frontmatter_start:frontmatter_end + 3]
                # print(self.frontmatter)

                # create a dict of the frontmatter content
                if self.frontmatter != None:
                    metadata_dict = {}
                    frontmatter = self.text.split("---")[1]
                    frontmatter = frontmatter.split("\n")

                    for item in frontmatter:
                        if item != '':
                            if "created: " in item:
                                metadata_dict["created"] = item[8:].strip()
                            else:
                                new_item = item.split(":")
                                metadata_dict[new_item[0]] = new_item[1].strip()
                    
                    try:
                        tags = metadata_dict["tags"][1:len(metadata_dict["tags"])-1].split(",")
                        tags = [tag.strip() for tag in tags]
                        if '' in tags:
                            tags.remove('')

                        metadata_dict["tags"] = tags

                    except KeyError:
                        metadata_dict["tags"] = []

                    self.metadata = metadata_dict

                    # tags as a single line string
                    if self.metadata["tags"] != []:
                        tags = ""
                        for tag in self.metadata["tags"]:
                            tags += "#" + tag + " "
                        self.tags = tags
                    else:
                        self.tags = ""

                    if "created" in self.metadata.keys():
                        self.created = self.metadata["created"]

                    else:
                        self.created = ""

            except IndexError:
                # Front matter not present.
                self.frontmatter = None
                self.metadata= None

                # Extract creation date
                if "Created: " in self.text:
                    self.created = self.text[self.text.find("Created: ") + 9:self.text.find("\n", self.text.find("Created: "))]
                else:
                    self.created = ""

                # Extract tags
                if "Tags: " in self.text:
                    tags_string = self.text[self.text.find("Tags:"):self.text.find("\n",self.text.find("Tags: ") + 6)]
                    self.tags = [tag.strip() for tag in tags_string.split("#") if "Tags:" not in tag]
                
                else:
                    self.tags = ""

                
            # title = the first line starting with '# ' after the front matter
            self.title = self.text[self.text.find("# ",frontmatter_end):self.text.find("\n",self.text.find("# ",frontmatter_end))][2:]
            
            # content = everything after the title
            # TODO Content needs to start AFTER the tag string.
            self.content = self.text[self.text.find("\n",self.text.find("# "))+1:]

        else:
            self.text = None

    def update(self):
        # write metadata, title and content to the file
        
        # Update the frontmatter string from the dict
        if self.metadata != None:
            new_frontmatter = "---\n"
            for key in self.metadata.keys():
                new_frontmatter += key + ": "
                if key.upper() == "TAGS":
                    new_frontmatter += str(self.metadata[key]).replace("'","") + "\n"
                else:     
                    new_frontmatter += self.metadata[key] + "\n"
            new_frontmatter += "---\n"
        else:
            new_frontmatter = ""

        with open(self.file_path,"w",encoding="utf-8") as f:
            if new_frontmatter != "":
                f.write(new_frontmatter)
            f.write("# " + self.title + "\n")
            if self.created != "":
                f.write("Created: " + self.created) 

            if self.tags != "":
                f.write(self.tags_string)

            f.write(self.content)

    def remove_frontmatter(self):
        self.metadata = None
        self.update()
    
    def set_title(self,new_title):
        self.title = new_title
        self.update()

    def fix_title(self):
        '''
        Set the title to match the filename.
        '''
        new_title = self.file_path.stem.replace("_"," ")
        self.set_title(new_title)

    def tags_to_content(self):
        """
        Remove the front matter and add date created and tags to content,
        below the title.
        """
        new_content = "# " + self.title + "\n\n"
        new_content += "Created: " + self.created + "\n"
        new_content += "Tags: " + self.tags + "\n\n"
        new_content += self.content
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write(new_content)
    
    def tags_string(self):
        tag_string = ""
        for tag in self.tags:
            tag_string += "#" + tag + " "
        return tag_string


    def replace_text(self,old_text,new_text):
        self.text = self.text.replace(old_text,new_text)     
        with open(self.file_path,"w",encoding="utf-8") as f:
            f.write(self.text)    

    
    
def review_files(target_dir):
    """
    Every Markdown file in the vault.
    """
    for item in target_dir.iterdir():
        if item.is_file() and item.suffix == ".md":
            new_file = ObsidianNote(item)
            if new_file.tags == [] and "Templates" not in str(item.parent):
                print(item.name)



        elif item.is_dir():
            review_files(item)    