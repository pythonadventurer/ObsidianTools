from pathlib import Path
from config import *

import zipfile
from datetime import datetime as dt

def zip_backup(source,dest):
    source = Path(source)
    dest = Path(dest)
    with zipfile.ZipFile(dest, mode="w") as archive:
        for file_path in source.rglob("*"):
            archive.write(file_path,
            arcname=file_path.relative_to(source))
    print("Backup completed.")

    
timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]

source = vault
dest = Path(vault_backup,timestamp + " DevNotes2.zip")

zip_backup(source,dest)

