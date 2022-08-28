from lib import *

vault_folder = r"D:\Rob\Compendium"


# print(my_file.file_id)
# print(my_file.category)
# print(my_file.topic_num)
# print(my_file.counter)
# print(my_file.topic_id)
# print(my_file.next_topic_id)
# print(my_file.next_counter)

my_vault = ObsidianVault(vault_folder)
# print(my_vault.category_folders)

for file in my_vault.numbered_files:
    print(file.file_name)


    






















