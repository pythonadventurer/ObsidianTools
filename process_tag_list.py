from config import *
from lib import *

test_resource_file = r"1963 Martin Luther King Jr  Letter from Birmingham.pdf"
test_resource_md = r"Animals.md"
# test_file_path = Path(resource_catalog, test_resource_md)

my_file = ObsidianNote(Path(notes_folder,test_resource_md))

my_file.set_title("Amazing Animals")
my_file.save()


















