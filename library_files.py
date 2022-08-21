from pathlib import Path

ObsidianLibrary = Path(r"D:\Rob\InfoCenter\Library")
PagesDir = Path(r"D:\Rob\InfoCenter\Library\Pages")

for item in ObsidianLibrary.iterdir():
    page_file_name = Path(PagesDir,item.stem + ".md")
    document_link = f"[[{item.name}]]"
    document_title = "# " + item.stem
    with open(page_file_name,"w",encoding='utf-8') as file:
        file.write(document_title + "\n\n" + document_link + "\n")
    print("Created file: " + str(page_file_name))
        

