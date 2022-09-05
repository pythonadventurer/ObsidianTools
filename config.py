import os
from pathlib import Path

if os.environ['COMPUTERNAME'] == 'DESKTOP-JNCQ9MB':
    vault_folder = Path(r"C:\Users\robf.PCS\Documents\DevNotes")
    projects = Path(r"C:\Users\robf.PCS\Documents\DevNotes\Projects\2022")
    old_projects = Path(r"C:\Users\robf.PCS\Documents\Notebook\Home\Projects\2022")

    converted_projects = Path(r"C:\Users\robf.PCS\Documents\converted_projects")
    

else:
    vault_folder = Path(r"D:\Rob\Vault")

to_file = Path(r"D:\Rob\_TO_BE_FILED\Library")
resource_folder = Path(r"D:\Rob\_TO_BE_FILED\Resources")
resource_catalog = Path(r"D:\Rob\Vault\Resources\Resource_Catalog")