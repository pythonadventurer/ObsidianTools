from config import *
from pathlib import Path

def zim_to_md(zim_file,output_dir):
    try:
        with open(zim_file,"r") as f:
            text = f.read()
        
    except UnicodeDecodeError:
        with open(zim_file,"r",encoding="utf-8") as f:
            text = f.read()   

    # eliminate zim header
    if zim_header in text:
        complete_header = text[:text.find("\n",60)]
        text = text.replace(complete_header,"")


    # split text into lines for more focused parsing
    text_lines = text.split("\n")
    new_text_lines = []

    for n in range(len(text_lines)):

        # extract title from rst formatted titles
        if text_lines[n].startswith("###"):
            title = text_lines[n-1]
        
        elif text_lines[n].startswith("# "):
            title = text_lines[n][2:]
        
        new_text_lines.append("# " + title)

    for n in range(len(text_lines)):
        # replace asterisk list bullets
        new_line = text_lines[n].replace("* ","- ")
        new_line = new_line.replace("o   "," - ")
        new_text_lines.append(new_text_line)
    
    new_text = "\n".join(new_text_lines)
    new_file = Path(notebook_output,title + ".md")
    with open(new_file,"w",encoding="utf-8") as new_file:
        new_file.write(new_text)
    print("Created new file: " + str(new_file))








    #     title = text_lines[:text_lines.find("\n###")]
    #     title_underline_start = text_lines.find("\n###") + 1
    #     title_underline_end = text_lines.find("\n",title_underline_start)
    #     title_underline = text_lines[title_underline_start:title_underline_end]
    #     text_lines = text_lines.replace(title_underline,"")

    # # extract title from markdown format
    # if text_lines.find("\n# ") != -1:


zim_to_md(Path(zim_dir,"Journal/2019/02/01.txt"),notebook_output)




