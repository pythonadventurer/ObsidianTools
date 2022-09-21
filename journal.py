from config import *
from datetime import datetime

# "\ufeff"
# strftime: %Y-%m-%d
# strftime with time" %Y-%m-%d %H:%M:%S
# strptime: %A, %B %d, %Y
# Prep Lifeline entries for Obsidian

def rename_entry(file_path):
    file_path = Path(file_path)    
    if file_path.suffix == ".txt":
        new_name = Path(file_path.parent,file_path.stem + ".md")
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
    new_lines = [title,"Created: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    new_lines.append("Tags: #Lifeline")
    new_lines.extend(content)
    new_text = "\n".join(new_lines)
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(new_text)
    print("Metatdata added to file: " + file_path.name)



    

# Create a list of the entries
entries = [entry for entry in journal_prep.iterdir()]

add_metadata(entries[0])





