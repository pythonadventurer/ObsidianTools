from lib import *
from config import *
from pathlib import Path


for file in resource_catalog.iterdir():
    fix_titles(file)