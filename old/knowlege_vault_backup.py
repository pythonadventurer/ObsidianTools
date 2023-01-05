from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = Path(r"D:\Rob\Knowledge_Vault")
dest = Path(Path(r"D:\Rob\Backups\Obsidian_backups"),timestamp + " knowledge-vault.zip")

zip_backup(source,dest)

