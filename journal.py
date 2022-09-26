from config import *
from datetime import datetime

# "\ufeff"
# strftime: %Y-%m-%d
# strftime with time" %Y-%m-%d %H:%M:%S
# strptime: %A, %B %d, %Y
# Prep Lifeline entries for Obsidian

def rename_entry(file_path):
    # rename Diarium entry to just "YYYY-MM-DD" plus .md
    file_path = Path(file_path)    
    if file_path.suffix == ".txt":
        new_name = Path(file_path.parent,file_path.stem[8:18] + ".md")
        file_path.rename(new_name)
        print("Renamed: " + file_path.name)


def re_save(file_path):
    # get rid of BOM
    file_path = Path(file_path)    
    with open(file_path,"r",encoding="utf-8-sig") as file:
        file_text = file.read()

    with open(file_path,"w",encoding="utf-8") as file:
        file.write(file_text)
        print("File: " + file_path.name + " converted to utf-8.")

def fix_entry_date(file_path):
    # Format the entry date and turn it into a title
    file_path = Path(file_path)    
    with open(file_path,"r",encoding="utf-8") as file:
        file_text = file.read().split("\n")
        if not(file_text[0].startswith("# ")):
            entry_date = datetime.strptime(file_text[0].strip(),"%A, %B %d, %Y").strftime("%Y-%m-%d")
            file_text[0] = "# " + entry_date
            new_text = "\n".join(file_text)
            with open(file_path,"w",encoding="utf-8") as file:
                file.write(new_text)

def add_metadata(file_path):
    # add Created date and tags
    file_path = Path(file_path)    
    with open(file_path,"r",encoding="utf-8") as file:
        lines = file.read().split("\n")
    title = lines[0]
    content = lines[1:]
    new_lines = [title,"\nCreated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    new_lines.append("Tags: #Lifeline\n")
    new_lines.extend(content)
    new_text = "\n".join(new_lines)
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(new_text)
    print("Metatdata added to file: " + file_path.name)



def process_entries(prep_dir):          
    # Create a list of the entries
    entries = [entry for entry in prep_dir.iterdir()]

    for entry in entries:
        if entry.suffix == ".txt":
            re_save(entry)
    
    for entry in entries:
        if entry.suffix == ".txt":
            rename_entry(entry)

    for entry in entries:
        fix_entry_date(entry)

    for entry in entries:
        add_metadata(entry)


process_entries(journal_prep)
