import config
from pathlib import Path
from lib import *



dest_dir = config.converted_projects

for item in config.old_projects.iterdir():
    if item.is_file():
        zim_to_md(item,dest_dir)