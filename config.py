import os
from pathlib import Path

computer_name =  os.environ['COMPUTERNAME']
completed_task = "- [x] #task 📅 "
open_task = "- [ ] #task 📅 "

if computer_name == "TUFFY":
    vault = Path(r"D:\Rob\Vault")
    vault_backup = Path(r"D:\Rob\Backups\Vault_backups")

else:
    vault = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2")
    vault_backup = Path(r"F:\devnotes")
    backend = Path(r"\\server\Access\Backend_v2")
    backend_backup = Path(r"F:\backend")
    docs = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents")
    docs_bkp = Path(r"F:\documents")



