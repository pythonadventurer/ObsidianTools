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


def rename_txt(file_path):
    # rename Diarium entry with filename "YYYY-MM-DD.txt"
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
    new_lines = [title,"\nCreated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    new_lines.append("Tags: #Lifeline\n")
    new_lines.extend(content)
    new_text = "\n".join(new_lines)
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(new_text)
    print("Metatdata added to file: " + file_path.name)


def combine_duplicates(file_path):
    """
    """
    file_path = Path(file_path)
    file_list = [item for item in file_path.iterdir() if item.is_file()]
    match = False
    duplicates = []
    for n in range(0,len(file_list)):

        # First, check if current = previous. The answer deteremines what is to be done.
        curr_file_name = file_list[n].stem[8:18]
        prev_file_name = file_list[n-1].stem[8:18]
        if curr_file_name == prev_file_name:
            new_file_name = curr_file_name + ".md"
            with open(file_list[n],"r",encoding="utf-8") as f:
                curr_text = f.read()

            # match = false means this is the first duplicate file date,
            # therefore need to get the previous text and add it to the
            # current.            
            if match == False:
                with open(file_list[n-1],"r",encoding="utf-8") as f:
                    prev_text = f.read()

                entry_text = curr_text + prev_text

                # Set match to True to prevent the first matching file text
                # from being overwritten by subsequent matches
                match = True

            elif match == True:
                # there has already been a prior match, so DON'T re-add the previous file's text again
                # just add the current text.
                entry_text += curr_text
        
        else:
            if match == True:
                new_file = Path(file_list[n].parent,new_file_name)
                with open(new_file,"w",encoding="utf-8") as f2:
                    f2.write(entry_text)
                    print(f"File:{new_file} created.")
                duplicates.append(new_file.stem)
                match = False

    # Delete the duplicate files
    for item in file_list:
        if item.name[8:18] in duplicates:
            item.unlink()
            print(f"File: {item.name} deleted.")

            


def process_entries(prep_dir):          
    # Create a list of the entries
    entries = [entry for entry in prep_dir.iterdir()]

    for entry in entries:
        new_name = Path(entry.parent,entry.stem[8:18] + ".md")
        entry.rename(new_name)


    # for entry in entries:
    #     if entry.suffix == ".txt":
    #         re_save(entry)
    
    # for entry in entries:
    #     if entry.suffix == ".txt":
    #         rename_txt(entry)

    # for entry in entries:
    #     if entry.suffix == ".md":
    #         fix_entry_date(entry)

    # for entry in entries:
    #     if entry.suffix == ".md":
    #         add_metadata(entry)

# combine_duplicates(journal_prep)

lifeline = Path(r"D:\Rob\my_vault\Lifeline")
for y in range(1981,2020):
    new_folder = Path(lifeline,str(y))
    new_folder.mkdir()
    