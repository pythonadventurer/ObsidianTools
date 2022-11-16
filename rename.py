from pathlib import Path

folder = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2\Databases\DataManager2\Changelog\2019")

for file in folder.iterdir():
    file.rename(Path(folder,"DM2_" + file.name))
    


