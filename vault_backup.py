from zip_backup import *
from config import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = vault
dest = Path(vault_backup,timestamp + " vault.zip")

zip_backup(source,dest)