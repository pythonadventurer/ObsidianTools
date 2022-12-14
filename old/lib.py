from pathlib import Path
import re
from time import sleep

# (?<=\[\[).+?(?=\]\])


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
    """
    The text of an ObsidianNote (ObsidianNote.text) has the following parts:
        - Frontmatter (optional). First element of note, must be
          bound by "---"
            - If frontmatter is present, it will contain the elements
              'Created' and 'Tags'.
        - Title (starts with "# ". Only one title per note.)
        - Creation date, prefixed with "Created: ". May be inside or outside the frontmatter.
        - Tags (optional, but "Tags: " required).  May be inside or outside the frontmatter.
        - Content : all of the text after the above four parts.
    An ObsidanNote object will have the following properties. All are strings except .tags, 
    which is a list. 
        ObsidanNote.text : all the text of the note, including the four parts.
        ObsidanNote.frontmatter : The frontmatter, as a string, including the "---" at
                                  start and end.
        ObsidanNote.title : The title of the note, without the "# " prefix.
        ObsidanNote.created : Creation date, as a string. Example:  2022-09-07 06:58:56.
        ObsidianNote.tags : Tags as a list, without the hashtags. No tags = empty list.
        ObsidanNote.content : All of Obsidian.text after the above four elements.

        All of these except .tags, if not present, will have the value of "" (empty string.)
    """
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
                    
            
            # check for frontmatter 
            if self.text[:3] == "---":
                self.frontmatter =  self.text[0:self.text.find("---",3)+3]
            
                # get the "Created" and "Tags" properties from the frontmatter.
                frontmatter = self.frontmatter.split("---")[1]
                frontmatter = frontmatter.split("\n")

                for item in frontmatter:
                    if item != '':
                        if "created: " in item:
                            self.created = item[8:].strip()
                        
                        elif "tags: " in item:
                            tags_string = item[7:len(item)-1].strip()
                            self.tags = [tag.strip() for tag in tags_string.split(",") if "Tags:" not in tag]
                
                # If frontmatter present, then content starts after the title
                content_start = self.text.find("\n", self.text.find("# "))

            else:
                # Front matter not present.
                self.frontmatter = ""
                
                # Extract creation date
                if "Created: " in self.text:
                    self.created = self.text[self.text.find("Created: ") + 9:self.text.find("\n", self.text.find("Created: "))]
                else:
                    self.created = ""

                # Extract tags from the note text
                if "Tags: " in self.text:
                    tags_string = self.text[self.text.find("Tags:"):self.text.find("\n",self.text.find("Tags: ") + 6)]
                    self.tags = [tag.strip() for tag in tags_string.split("#") if "Tags:" not in tag]
                
                else:
                    self.tags = []
                
                # If no frontmatter, content starts after the tags line
                content_start = self.text.find("\n", self.text.find("Tags: ")) + 1
                
            # title = the first line starting with '# ' 
            self.title = self.text[self.text.find("# ") + 2:self.text.find("\n",self.text.find("# "))]

            self.content = self.text[content_start:]

        else:
            self.text = None

    def write_file(self):
        # write metadata, title and content to the file

        with open(self.file_path,"w",encoding="utf-8") as f:
            if self.frontmatter != "":
                f.write(self.frontmatter + "\n")
            f.write("# " + self.title + "\n\n")
            f.write("Created: " + self.created + "\n")
            f.write("Tags: " + self.tags_string() + "\n")
            f.write(self.content)

    def fix_title(self):
        '''
        Set the title to match the filename.
        '''
        new_title = self.file_path.stem.replace("_"," ")
        self.title = new_title

    def tags_string(self):
        # convert tags from list to string, for writing to file
        tag_string = ""
        for tag in self.tags:
            tag_string += "#" + tag + " "
        return tag_string

class ObsidianVault:
    '''
    For doing stuff that applies to a complete Obsidian vault.
    '''
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.files = []
        self.tags = []
        self.linked_files = []
        self.review_files(self.file_path)

    def review_files(self,file_path):
        for item in file_path.iterdir():
            if item.is_file() and item.suffix == ".md":
                self.files.append(item.name)
                with open(item,"r",encoding = "utf-8") as f:
                    file_text = f.read()

                if "Tags: " in file_text:
                    tags_string = file_text[file_text.find("Tags: ")+6:file_text.find("\n",file_text.find("Tags: "))]
                    tags = [tag.replace("#","").strip() for tag in tags_string.split(" ")]
                    for tag in tags:
                        if tag not in self.tags:
                            self.tags.append(tag)
                link_pattern = "(?<=\[\[).+?(?=\]\])"
                if re.findall(link_pattern, file_text) != None:
                    for file in re.findall(link_pattern, file_text):
                        if file not in self.linked_files:
                            self.linked_files.append(file)
                            



            elif item.is_dir():
                self.review_files(item)
        self.tags.sort()
        self.linked_files.sort()
        

def bulk_tag(tag, target_dir):
    """
    add tag to all untagged files
    """
    for item in Path(target_dir).iterdir():
        if item.is_file() and item.suffix == ".md":
            new_file = ObsidianNote(item)
            if "Templates" not in str(item.parent) and new_file.tags == ['']:
                print(item.name)
                new_file.tags = [tag]
                new_file.write_file()
                
        elif item.is_dir():
            bulk_tag(tag, item)


def bulk_tag_replace(find_tag, replace_tag, target_dir):
    """
    replace tag
    """
    for item in Path(target_dir).iterdir():
        if item.is_file() and item.suffix == ".md":
            new_file = ObsidianNote(item)
            if "Templates" not in str(item.parent) and find_tag in new_file.tags:
                print(item.name)
                new_file.tags.remove(find_tag)
                new_file.tags.append(replace_tag)
                new_file.write_file()
                
        elif item.is_dir():
            bulk_tag_replace(find_tag, replace_tag, item)