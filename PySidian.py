from config import *
from pathlib import Path

class ObsidianNote(VaultPath):
	"""
	Every ObsidianNote is associated with a VaultPath (the top level directory
	of an Obsidian vault.)

	"""
	def __init__(self):
		self.vault = VaultPath
		self.metadata = {}
		self.content = ""
		self.filename = "Untitled.md"
		

	def read_note(self, NotePath):
		"""
		Read metadata and content from an existing note.
		"""
		with open(NotePath,"r",) as file:
			self.metadata, self.content = frontmatter.parse(file.read())

		self.filename = Path(NotePath).name

