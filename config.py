from pathlib import Path
import os

if os.environ['COMPUTERNAME'] == "DESKTOP-JNCQ9MB":
	current_vault = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes2")
	new_vault = Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\DevNotes3")
	backup_dir = \
		Path(r"C:\Users\Robf.DESKTOP-JNCQ9MB\Documents\ObsidianBackups")
else:
	current_vault = Path(r"D:\Rob\Knowledge_Vault")


