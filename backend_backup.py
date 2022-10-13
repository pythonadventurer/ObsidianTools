from zip_backup import *
from config import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = backend
dest = Path(backend_backup,timestamp + " Backend.zip")

zip_backup(source, dest)

