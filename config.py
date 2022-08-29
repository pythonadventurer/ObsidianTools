import os
from pathlib import Path

if os.environ['COMPUTERNAME'] == 'DESKTOP-JNCQ9MB':
    vault_folder = Path(r"C:\Users\robf.PCS\Documents\Compendium")

else:
    vault_folder = Path(r"D:\Rob\Compendium")

to_file = Path(vault_folder, r"06_Library\TO_FILE")
