import config
from pathlib import Path
from lib import *


zim_file = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022\2022-01-05_Eliminate_DupTest_Field.txt")
dest_dir = config.converted_projects

for item in config.projects.iterdir():
    if item.is_file():
        zim_to_md(item,dest_dir)