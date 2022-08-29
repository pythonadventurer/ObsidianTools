import config
from lib import *
    
my_vault = ObsidianVault(config.vault_folder)

for file in my_vault.numbered_files:
    print(file.file_name)





















