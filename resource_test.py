from config import *
from lib import *

test_resource_file = r"1963 Martin Luther King Jr  Letter from Birmingham.pdf"

# test_file_path = Path(resource_catalog, test_resource_md)

my_file = ObsidianResource(Path(to_file, test_resource_file))

print(my_file.metadata_file)

















