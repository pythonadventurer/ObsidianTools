from pathlib import Path
import zipfile
from datetime import datetime as dt


def backup(source,dest):
	"""
	A simple zip backup utility.
	"""
	source = Path(source)
	dest = Path(dest,Path(source).name + "-" + file_timestamp() + ".zip")
	print(f"Backing up {source} to {dest}....")
	with zipfile.ZipFile(dest, mode="w") as archive:
	    for file_path in source.rglob("*"):
	        archive.write(file_path,
	        arcname=file_path.relative_to(source))
	print("Backup completed.")


def file_timestamp():
	"""
	Time stamp utility designed for date-based naming of files.
	Format: YYYY-MM-DD-HHMMSS.
	"""
	return str(dt.now()).replace(" ","-").replace(":","")[:17]

def meta_timestamp():
	return dt.now().strftime('%Y-%m-%d %H:%M:%S')
