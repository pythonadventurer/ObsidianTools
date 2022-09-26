from config import *
from lib import *

# \[\[(.*?)\]\]
# (?<=\[).+?(?=\])


my_vault = ObsidianVault(vault)

for file in my_vault.linked_files:
    print(file)
    