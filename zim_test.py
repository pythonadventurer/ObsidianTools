import config
from pathlib import Path
from lib import *

test_file = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022\2022-03-25_Membership_Procedures.txt"

dest_dir = config.converted_projects

zim_to_md(test_file,dest_dir)