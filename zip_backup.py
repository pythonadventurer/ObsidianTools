from pathlib import Path


import zipfile
from datetime import datetime as dt

def zip_backup(source,dest):
    source = Path(source)
    dest = Path(dest)
    print(f"Backing up {source} to {dest}....")
    with zipfile.ZipFile(dest, mode="w") as archive:
        for file_path in source.rglob("*"):
            archive.write(file_path,
            arcname=file_path.relative_to(source))
    print("Backup completed.")

    

