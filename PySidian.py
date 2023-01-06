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

	def add_metadata(self, key, value):
		"""
		If the key already exists in the metadata, its value will
		be replaced.
		"""	
		self.metadata[key] = value

	def add_tag(self,tag):
		if "tags" in self.metadata.keys():
			self.metadata["tags"].append(tag)
		else:
			self.metadata["tags"] = ["tag"]


	def read_note(self, NotePath):
		"""
		Read metadata and content from an existing note.
		"""
		try:
			with open(NotePath,"r",) as file:
				self.post = frontmatter.load(file)
		except UnicodeDecodeError:
			with open(NotePath,"r",encoding = "utf-8") as file:
				self.post = frontmatter.load(file)	

		self.filepath = Path(NotePath)
		self.metadata = self.post.metadata
		self.content = self.post.content

	def remove_metadata(self,key):
		if key in self.metadata.keys():
			del self.metadata[key]

	def remove_tag(self,tag):
		if "tags" in self.metadata.keys():
			if tag in self.metadata["tags"]:
				self.metadata["tags"].remove(tag)

	def write_note(self):
		"""
		"""
		# update the frontmatter.post object for writing
		self.post.metadata = self.metadata
		self.post.content = self.content
		with open(self.filepath,"w",encoding="utf-8") as file:
			text = frontmatter.dumps(self.post)	
			file.write(text)
