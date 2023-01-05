from zip_backup import *

timestamp = str(dt.now()).replace(" ","-").replace(":","")[:17]
source = Path(r"D:\Rob\Exercise_Log")
dest = Path(Path(r"D:\Rob\Backups\Obsidian_backups"),timestamp + " exercise-log.zip")

zip_backup(source,dest)

