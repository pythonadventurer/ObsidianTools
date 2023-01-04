from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = docs
dest = Path(r"\\server\Rob\backups\rob_documents",timestamp + " Documents.zip")

zip_backup(source,dest)