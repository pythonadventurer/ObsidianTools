from config import *
from pathlib import Path
import frontmatter

class Note:
	"""
	A note has two components: Note.metadata and Note.content.
	content is the note's text, so it is a string that can be manipulated
    with Python string methods.  metadata is a dictionary.



	"""
	def __init__(self):
		self.filepath = Path(Path.cwd(),"Untitled.md")
		self.post = frontmatter.loads("")
		self.metadata = {}
		self.content = ""
		

	def read_note(self, NotePath):
		"""
		Read metadata and content from an existing note.
		"""
		with open(NotePath,"r",) as file:
			self.post = frontmatter.load(file)

		self.filepath = Path(NotePath)
		self.metadata = self.post.metadata
		self.content = self.post.content


	def write_note(self):
		"""
		"""
		# update the frontmatter.post object for writing
		self.post.metadata = self.metadata
		self.post.content = self.content
		with open(self.filepath,"w") as file:
			text = frontmatter.dumps(self.post)	
			file.write(text)
