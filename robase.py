
from config import *
from datetime import datetime as dt
import os
import re
import shutil

class Note:
	"""
	Create a new Note.
	A Note has two text blocks: metadata_text and body text.
	Metadata text is standard YAML, such as that used by apps such as Obsidian and
    VS code.
	The note's metadata can be accessed like a dictionary.  Example:
		Note.metadata["title"] = "my_title
	"""
	def __init__(self):
		self.metadata = {}

		# When used, these items will always appear in this order, at the top.
        # Items in metadata that are not in this list will be added after these
		# items.
		self.meta_order = ["file-id",
						   "created",
						   "tags",
						   "author",
						   "source"]
		self.write_metadata()
		self.body_text = ""

	def add_metadata(self, key, value):
		"""
		update the metadata text whenever a new item is added.
		"""
		self.metadata[key] = value
		self.write_metadata()

	def add_tag(self,tag):
		if "tags" in self.metadata.keys():
			self.metadata["tags"].append(tag)
		else:
			self.metadata["tags"] = [tag]
		self.write_metadata()

	def convert_wk_links(self):
		"""
		Convert WikiLinks to Markdown links:
		Example:

			From:
			[[GigaSecure_tech_notes.png]]

			To:
			[GigaSecure_tech_notes.png](GigaSecure_tech_notes.png)
		"""
		links = self.get_wiki_links()	
		for link in links:
			link_filename = re.search("\[\[(.+)\]\]",link).group(1)
			link_start = self.body_text.find(link)
			new_link = f"[{link_filename}]({link_filename})"
			
			# check if file is embedded, and if so, add "!"
            # to front of link.
			if link_start == "!":
				new_link = "!" + new_link
			self.body_text = self.body_text.replace(link, new_link)

	def created(self):
		if "created" in self.metadata.keys():
			return self.metadata["created"]
		else:
			return None

	def delete_metadata(self,key):
		"""
		Remove an item from metadata and rewrite to metadata_text.
		NOTE: If key == "tag" or "tags", ALL tags will be removed!
		To remove an individual tag, use Note.remove_tag.
		"""
		if key in self.metadata.keys():		
			del(self.metadata[key])
			self.write_metadata()

	def delete_metadata_text(self, text_block):
		"""
		remove metadata text from a block of text.
		"""
		if text_block[:3] == "---":
			note_metadata = text_block[:text_block.find("---",4)+4]
			text_block = text_block.replace(note_metadata,"")

		return text_block

	def delete_tag(self,tag):
		if tag in self.metadata["tags"]:
			self.metadata["tags"].remove(tag)
			self.write_metadata()

	def extract_linked_files(self,link_list, source_dir, dest_dir):
		"""
		Copy the linked embedded files to the dest_dir.
		This works for both Markdown and WikiLinks.
		"""
		for link in link_list:
			file_name = link.replace("[","")
			file_name = file_name.replace("]","")
			file_name = file_name.replace("(","")
			file_name = file_name.replace(")","")
			file_name = file_name.replace("!","")
			file_name = Path(file_name).name
			shutil.copy2(Path(source_dir,file_name),Path(dest_dir,file_name))
			print(f"Copied embedded file: {file_name}")

	def file_id(self):
		if "file-id" in self.metadata.keys():
			return self.metadata["file-id"]
		else:
			return None

	def get_created_time(self,file_path):
		ctime = file_path.stat().st_ctime
		ctime = dt.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
		return ctime

	def get_metadata(self,key):
		if key in self.metadata.keys():
			return self.metadata[key]

		else:
			return None

	def get_md_links(self):
		"""
		Get the existing Markdown-style links to embedded files.
		"""
		link_list = re.findall("\[.+\)", self.body_text)

		return link_list

	def get_wiki_links(self):
		"""
		Get the existing Wiki-style links to embedded files.
		"""
		link_list = re.findall("\[\[.+\]\]", self.body_text)
		return link_list

	def get_linked_file_list(self):
		linked_file_list = re.findall("\!\[\[(.+)\]\]", self.body_text)
		return linked_file_list

	def read_metadata(self,text):
		"""
`		Read metadata from a block of text. Overwrites all existing metadata.
		Note this could be used to read metadata from an external file
        as well as the note's text itself.
		"""
		if text[:3] == "---":
			self.metadata = {}
			note_metadata = text[:text.find("---",4)+3]
			note_metadata = note_metadata.replace("---","")
			note_metadata = note_metadata.split("\n")
			
			for item in note_metadata:
				split_item = item.split(": ")
				if split_item != ['']:

					# tags are to be a list
					if split_item[0] == "tags":
						self.metadata["tags"] = split_item[1]
						if self.metadata["tags"] == "[]":
							self.metadata["tags"] = []
					else:
						self.metadata[split_item[0]] = split_item[1]
			
	def read_note(self,file_path):
		"""
		Reads text from another note, overwriting the note's existing metatadata and body text.
		"""
		try:
			with open(file_path,"r") as file:
				all_text = file.read()

		except UnicodeDecodeError:
			with open(file_path,"r",encoding="utf-8") as file:
				all_text = file.read()

		self.read_metadata(all_text)
		self.write_metadata()
		self.body_text = self.delete_metadata_text(all_text)


		# check for a title in the body text. If it exists, add it
		# to the metadata.  If no title in the body text, assign the
		# file name as the title.
		title_text = re.match("^# (.+)\n",self.body_text)
		if "title" not in self.metadata.keys():
			if title_text != None:
				self.metadata["title"] = title_text[1].replace(":"," - ")
			else:
				self.metadata["title"] = file_path.stem


	def source(self):
		if "source" in self.metadata.keys():
			return self.metadata["source"]
		else:
			return None

	def tags(self):
		if "tags" in self.metadata.keys():
			return self.metadata["tags"]
		else:
			return None

	def title(self):
		if "title" in self.metadata.keys():
			return self.metadata["title"]
		else:
			return None

	def write_metadata(self):
		"""
		writes metadata to metadata_text
		"""
		self.metadata_text = "---\n"
		items = []

		# first, write out the items that exist in the meta_order list, and keep
        # track of these items.
		for item in self.meta_order:
			if item in self.metadata.keys():
				if item == "tags":
					self.metadata_text += "tags: " + str(self.metadata["tags"]).replace("'","") + "\n"				

				else:
					self.metadata_text += item + ": " + self.metadata[item] + "\n"

				items.append(item)

		# write out items that are not in meta_order by skipping those that
        # have already been aded.
		for item in self.metadata.keys():
			if item not in items:
				self.metadata_text += item + ": " + self.metadata[item] + "\n"

		self.metadata_text += "---\n"

	def write_note(self,file_path):
		"""
		Write out the note content to a Markdown file.
        Automatically updates the note's metadata from 
	    Note.metadata.
		"""
		with open(file_path,"w",encoding="utf-8") as file:
			created = self.get_created_time(file_path)
			self.add_metadata("created", created)
			self.write_metadata()
			self.write_title()
			all_text = self.metadata_text + self.body_text.strip()
			file.write(all_text)

		print(f"Note {file_path} created.")

	def write_title(self):
		"""
		Add the title from metadata (if exists) to the top line of the
		body text, formatted as header level 1. Overwite existing title in
		the body text, if it exists. 
		If there is no title in the metadata, but the body text contains a
		title, it will not be affected.
		"""
		title_text = re.match("^# (.+)\n",self.body_text)
		if "title" in self.metadata.keys():
			if title_text != None:
				self.body_text = self.body_text.replace(title_text[1],self.metadata["title"])
			else:
				self.body_text = "# " + self.metadata["title"] + "\n" + self.body_text

def sanitize_file_name(file_name):
	"""	
	Remove yucky characters from file name
	"""
	remove_chars = [" ","_","'",":","&",";","@","?","!",",","’"]
	for char in remove_chars:
		file_name = file_name.replace(char,"-")
	return file_name

def get_file_by_id(file_id, folder):
	# Retrieve a file by specifying only its 6 digit file ID.
	for item in Path(folder).iterdir():
		if item.is_file():
			if item.name[:10] == file_id:
				new_note = Note()
				new_note.read_note(item)
				return new_note


def new_file_id(id_file):
	with open(id_file,"r") as file:
		file_id = str(int(file.read().strip()) + 1).zfill(6)
	
	with open(id_file,"w") as file:
		file.write(file_id)

	return file_id + "-000"

def process_linked_files(note_path, files_path):
	"""
	If an existing Note contains links to files, copy the files
	to the note's directory, assigning each file a new file name 
	based on the note's file Id and name. Example:
		Note file:
			123456-000-dont-be-ashamed-of-your-scars.md

		Linked file:
			scars.jpg

		New inked file:
        	123456-001-scars.jpg

	"""
	note = Note()
	note.read_note(note_path)
	links = note.get_md_links()
	linked_files = note.get_linked_file_list()
	attachment_count = 1
	for linked_file in linked_files:
		existing_linked_file = Path(files_path,linked_file)
		new_linked_file_name = note.metadata["file-id"][:6] + "-" + str(attachment_count).zfill(3) + "-" + existing_linked_file.name
		attachment_count += 1
		new_linked_file_path = Path(note_path.parent,new_linked_file_name)
		shutil.copy2(existing_linked_file,new_linked_file_path)

def process_file(file_path, dest_dir):
	new_note = Note()
	new_file_name = sanitize_file_name(file_path.stem)
	if file_path.suffix == ".md":
		new_note.read_note(file_path)		
		# get rid of sets of 3 dashes in body text so it won't resemble metadata.
		new_note.body_text = new_note.body_text.replace("---","")

		new_note.add_metadata("created", dt.now().strftime('%Y-%m-%d %H:%M:%S'))

		# Get rid of old file_id (underscore instead of dash)	
		new_note.delete_metadata("file_id")
		
		# Assign a file id with suffix "-000"
		new_note.add_metadata("file-id", new_file_id(id_file))
		new_file_path = Path(dest_dir, new_note.metadata["file-id"] + "-" + new_file_name + ".md")

		new_note.write_note(new_file_path)
		os.remove(file_path)

	elif file_path.suffix.upper() == ".PDF" or file_path.suffix.upper() == ".JPG" or file_path.suffix.upper() == ".PNG":
		# Assign the pdf or jpg file a file ID with an attachment number, and
		# create an informational note with links to the file, and embeds.
		# New note = the informational note.
		title = file_path.stem
		attachment_count = 1
		new_note.add_metadata("file-id", new_file_id(id_file))
		new_note.add_metadata("title", title)
		new_note.add_metadata("tags",[])
		new_file_path = Path(dest_dir, new_note.metadata["file-id"] + "-" + new_file_name + ".md")
		new_attachment_name = new_note.metadata["file-id"][:6] + "-" + str(attachment_count).zfill(3) + "-" + new_file_name + file_path.suffix
		new_attachment_path = Path(dest_dir,new_attachment_name)
		shutil.copy2(file_path,new_attachment_path)
		file_link = f"[{title}]({new_attachment_name})"
		embed_link = "!" + file_link
		info_file_template = f"# {title}\n\n## Notes\n\n## Excerpt\n\n## Link\n{file_link}\n\n{embed_link}\n\n"
		new_note.body_text = info_file_template
		new_note.write_note(new_file_path)
		os.remove(file_path)

	print(f"Processed: {file_path.name}")

def batch_process(source_dir,dest_dir):
	"""
	Process a batch of Markdown files
	"""
	for file in source_dir.iterdir():
		if file.suffix == ".ini":
			continue
		else:
			process_file(file, dest_dir)

def batch_tag(src_dir,tag):
	"""
	Apply a tag to a group of files
	"""
	for note in Path(src_dir).iterdir():
		if note.suffix == ".md":
			new_note = Note()	
			new_note.read_note(note)
			new_note.add_tag(tag)
			new_note.write_note(note)

