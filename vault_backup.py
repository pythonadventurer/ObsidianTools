from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = vault
dest = Path(vault_backup,timestamp + " my_vault.zip")

zip_backup(source,dest)