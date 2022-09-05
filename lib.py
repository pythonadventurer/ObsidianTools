from pathlib import Path
import re
import sys
import os


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


def add_tag(md_file,tag):
    with open(Path(md_file),"r") as f:
        content = f.read()
        if "tags: []" in content:
            content = content.replace("tags: []",f"tags: [{tag}]")
            with open(Path(md_file),"w") as f:
                f.write(content)     

            print(f"Added tag '{tag}' to file {md_file.name}")

    
def fix_titles(md_file):
    # match titles with filenames.
    with open(md_file,"r") as f:
        content = f.read()
        current_title = content[content.find("# [[")+4:content.find("]]")]
    content = content.replace("# [[" + current_title + "]]","# " + md_file.stem)    
    with open(md_file,"w") as f:
        f.write(content)
    print(f"Corrected title in: {md_file.name}")




