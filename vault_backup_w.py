from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = vault_w
dest = Path(vault_w_backup,timestamp + " DevNotes2.zip")

zip_backup(source,dest)