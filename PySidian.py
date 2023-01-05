from config import *
from pathlib import Path
import frontmatter

class Note:
	"""
	VaultPath = the top level directory of an Obsidian vault.
	Defaults to working directory.

	A note has two components: ObsidianNote.metadata and ObsidianNote.content.
	content is the note's text, so it is a string that can be manipulated
    with Python string methods.  metadata is a dictionary.



	"""
	def __init__(self,VaultPath=Path.cwd()):
		self.vault = VaultPath
		self.metadata = {}
		self.content = ""
		self.filename = "Untitled.md"
		

	def read_note(self, NotePath):
		"""
		Read metadata and content from an existing note.
		"""
		with open(NotePath,"r",) as file:
			self.post = frontmatter.load(file)

		self.filename = Path(NotePath).name
		self.metadata = self.post.metadata
		self.content = self.post.content


	def write_note(self):
		"""
		"""
		# update the post object for writing
		self.post.metadata = self.metadata
		self.post.content = self.content
		with open(Path(self.vault,self.filename),"w") as file:
			text = frontmatter.dumps(self.post)	
			file.write(text)
