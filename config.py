import os
from pathlib import Path

if os.environ['COMPUTERNAME'] == 'DESKTOP-JNCQ9MB':
    vault_folder = Path(r"C:\Users\robf.PCS\Documents\DevNotes")
    projects = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes\Projects")
    old_projects = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022")
    converted_projects = Path(r"C:\Users\robf.PCS\Documents\converted_projects")
    

else:
    vault_folder = Path(r"D:\Rob\Compendium")

to_file = Path(vault_folder, r"06_Library\TO_FILE")
completed_task = "- [x] #task 📅 "
open_task = "- [ ] #task 📅 "

to_file = Path(r"D:\Rob\_TO_BE_FILED\Library")
resource_folder = Path(r"D:\Rob\_TO_BE_FILED\Resources")
resource_catalog = Path(r"D:\Rob\Vault\Resources\Resource_Catalog")