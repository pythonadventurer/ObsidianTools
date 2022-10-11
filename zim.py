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

    # replace asterisk list bullets
    text = text.replace("* ","- ")
    text = text.replace("o   "," - ")

    # replace problem characters
    text = text.replace('‘','"')
    text = text.replace('’','"')

    # replace rst headers
    rst_start = text.find("\n===")
    if rst_start != -1:
        rst_end = text.find("=\n",rst_start) + 1
        rst_header = text[rst_start:rst_end]
        header_length = len(rst_header)
        header_start_index = rst_start - header_length
        header_text = text[header_start_index:rst_start]
        text = text.replace(header_text + rst_header,"## " + header_text + "\n"
    
        

    

zim_to_md(Path(zim_dir,"Journal/2019/01/28.txt"),notebook_output)



