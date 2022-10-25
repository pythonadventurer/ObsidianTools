from config import *
from obsidian import *
from pathlib import Path

src_file = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Databases\DataManager2\User Documentation\Main_Switchboard.md")

my_note = ObsidianNote(src_file)

wikilinks = my_note.get_wikilinks()

for link in wikilinks:
    new_link = re.search("\[\[(.+)\]\]",link)[1]
    new_link_source = new_link.replace(" ","_") + ".md"
    md_link = my_note.create_md_link(new_link, new_link_source)
    my_note.replace_text(link, md_link)



