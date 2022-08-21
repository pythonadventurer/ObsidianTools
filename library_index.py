from pathlib import Path

ObsidianLibraryIndex = Path(r"D:\Rob\InfoCenter\Library\Pages\_Index.md")
PagesDir = Path(r"D:\Rob\InfoCenter\Library\Pages")

with open(ObsidianLibraryIndex,"a",encoding='utf-8') as file:
    for page in PagesDir.iterdir():
        page_link = "[[" + page.stem + "]]\n"
        file.write(page_link)
        print("Added link: " +  page_link)

        

