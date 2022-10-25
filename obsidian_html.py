import markdown
from pathlib import Path

my_doc = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Databases\DataManager2\User Documentation\Main_Switchboard.md")

with open(my_doc,"r",encoding="utf-8") as f:
    text = f.read()
    html = markdown.markdown(text)

with open (Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Databases\DataManager2\User Documentation\HTML\Main_Switchboard.html"),"w",encoding="utf-8") as f:
    f.write(html)


