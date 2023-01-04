from config import *
from pathlib import Path
import frontmatter
import yaml

"""
experiments with Python libraries that can handle Obsidian frontmatter!
See: https://python-frontmatter.readthedocs.io/en/latest/

"""
my_text = """
author: Moi
tags:
 - Cool_Notes
 - Daily_Notes
 - Notes_of_Awesomeness
title: My_Best_Note_Ever
"""


my_fm_file = Path(vault_root, "01-Inbox","2023-01-04.md")

with open(my_fm_file,"r",encoding="utf-8") as file:
	metadata, content = frontmatter.parse(file.read())

print(metadata)
print(content)

