import zipfile
from datetime import datetime as dt
from pathlib import Path

task_start = "\U0001f6eb" # airplane
task_scheduled = "\U000023f3" # hourglass
task_due = "\U0001f4c5" # calendar icon 
task_done = "\U00002705" # green checkbox

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
	"""
	Human-friendly time stamp for use with Obsidan note metadata, such as
	creation date, update date, etc.
	"""
	return dt.now().strftime('%Y-%m-%d %H:%M:%S')


def fix_task_icons(text):
	"""
	Restores task icons when they are mysteriously turned into gibberish,
	even though the file is read with encoding set to UTF-8.
	"""
	text = text.replace("ðŸ›«",task_start)
	text = text.replace("ðŸ“…",task_due)
	text = text.replace("âœ…",task_done)
	return text
