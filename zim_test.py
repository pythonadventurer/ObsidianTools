import config
from pathlib import Path
from lib import *

test_file = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022\2022-03-25_Membership_Procedures.txt")

projects_old = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022")
projects_dir = Path(r"C:\Users\robf.PCS\Documents\DevNotes\Project_Archives\2022")
dest_dir = config.converted_projects

# for item in projects_dir.iterdir():
#     if item.is_file():
#         zim_to_md(item,dest_dir)

fix_tag(projects_dir)
