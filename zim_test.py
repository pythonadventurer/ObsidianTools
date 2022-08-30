import config
from pathlib import Path
from lib import *


zim_header = "====== 2022-02-14 Replace LogAppend with SendToLog ======"

dest_dir = Path(r"C:\Users\robf.PCS\Documents\converted_projects")
# for item in config.projects.iterdir():
#     if item.is_file():
#         zim_to_md(item, dest_dir)

my_vault = ObsidianVault(config.vault_folder)
my_vault.remove_file_ids(my_vault.vault_folder)



