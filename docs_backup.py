from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = docs
dest = Path(docs_bkp,timestamp + " Documents.zip")

zip_backup(source,dest)