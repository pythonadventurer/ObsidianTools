import re
from datetime import datetime as dt
from config import *
from pathlib import Path

def remove_zim_header(text):
    text = text.replace("Content-Type: text/x-zim-wiki","")
    text = text.replace("Wiki-Format: zim 0.6","")
    text = text.replace("Wiki-Format: zim 0.4","")
    for line in text.split("\n"):
        if line.startswith("Creation-Date:"):
            text = text.replace(line,"")
    
    return text

def remove_hash_lines(text):
    for line in text.split("\n"):
        if line.startswith("#####"):
            text = text.replace(line,"")

    for line in text.split("\n"):
        if line.startswith("======"):
            text = text.replace(line,"")    

    return text

def convert_rst_heading(heading_char,md_num,text):
    """
    Convert ReStructuredText headings to Markdown headings.
        heading_char : the character used to specify the header
                      level. Usually: "#","=","-","~"
        md_num : Markdown level to assign to the header.
                 1 = "#", 2 = "##", etc.
        text : the text containing the headings to be converted.
    """
    
    h = re.compile("(.+)\n" + heading_char + "+\n")
    match = h.findall(text)
    for heading in match:
        text = text.replace(heading + "\n" + len(heading) * heading_char,"#" * md_num + " " + heading)
    return text

def convert_zim_headings(text):
    zim_h2 = re.compile("===== (.+) =====")
    zim_h3 = re.compile("==== (.+) ====")

    match = zim_h2.findall(text)
    if match != None:
        for heading in match:
            text = text.replace("===== " + heading + " =====", "## " + heading)

    match = zim_h3.findall(text)
    if match != None:
        for heading in match:
            text = text.replace("==== " + heading + " ====", "### " + heading)
    
    return text


def get_title(title_char, text):
    """
    Extract a RST or ZimWiki formatted title.
    and below. Example:

    ##################################
    2019-10-28 The Results Review Form
    ##################################

    or:

    2019-10-28 The Results Review Form
    ##################################

    or

    ====== 2019-12-03 ======
    """
    # double line title
    t1 = re.compile(title_char + "+\n(.+)\n" + title_char + "+")

    # single line title
    t2 = re.compile("(.+)\n" + title_char + "+\n")

    # Zim title
    t3 = re.compile("=+ (.+) =+\n")


    match1 = t1.search(text)
    match2 = t2.search(text)
    match3 = t3.search(text)

    if match1 != None:
        title = match1.group(1)
        text = text.replace(title_char * len(title) + "\n" + title + "\n" + title_char * len(title),
                            "# " + title)        
            
    elif match2 != None:
        title = match2.group(1)
        text = text.replace(title + "\n" + title_char * len(title),
                    "# " + title)

    elif match3 != None:
        title = match3.group(1)
        text = text.replace(f"====== {title} ======","# " + title)
    
    else:
        title = ""
    
    return text
        

def md_title(text):
    """
    Return a Markdown title from the text.
    Must be a line starting with "# ".
    """
    for line in text.split("\n"):
        if line.startswith("# "):
            title = line[2:]

            return title
    
def fix_problem_chars(text):
    """
    Replace problematic characters:
        Open smart quote : â€˜
        Close smart quote : â€™
        Bullet dot : â€¢
        Dash : â€“

    """
    problem_chars =[['â€˜','"'],
                   ['â€™','"'],
                   ['â€¢','-'],
                   ['â€“','-'],
                   ["* ","- "]]
                   

    for char in problem_chars:
        text = text.replace(char[0],char[1])

    return text

def fix_todos(text):
    text = text.replace("[ ] TODO","- [ ] #task")
    text = text.replace("[*] TODO","- [x] #task")
    text = text.replace("[*] ","- [x] #task ")
    return text


def zim_to_md(zim_file, output_dir):
    try:
        with open(zim_file,"r") as f:
            text = f.read()
        
    except UnicodeDecodeError:
        with open(zim_file,"r",encoding="utf-8") as f:
            text = f.read()   

    text = remove_zim_header(text)
    text = fix_problem_chars(text)
    text = get_title("#",text)
    # title = md_title(text)
    # text = convert_rst_heading("=",2,text)
    # text = convert_rst_heading("+",3,text)
    text = convert_rst_heading("-",4,text)
    text = convert_zim_headings(text)
    text = fix_todos(text)
    # if len(title) > 10:  # if the title is a Zim date, and not YYYY-MM-DD
    #     new_title = dt.strftime(dt.strptime(title,"%A %d %b %Y"),"%Y-%m-%d")
    #     text = text.replace(title, new_title)
    #     title = md_title(text)
    text = remove_hash_lines(text)
    text = text.strip()
    
    # file_name = Path(output_dir,title + ".md")
    file_name = Path(output_dir,zim_file.stem + ".md")
    with open(file_name,"w",encoding="utf-8") as f:
        f.write(text)

    print("Created file: " + file_name.name)

def strip_file_names(dir):
    for item in Path(dir).iterdir():
        if item.is_file():
            new_name = item.name[:10] + ".md"
            item.rename(Path(item.parent,new_name))
            print("Renamed: " + new_name)

def process_zim_files(zim_dir,output_dir):
    for file in Path(zim_dir).iterdir():
        if file.suffix == ".txt":
            zim_to_md(file, output_dir)


process_zim_files(zim_dir, notebook_output)

# zim_to_md(zim_test_file, notebook_output)








