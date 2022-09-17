from config import *
from lib import *
from pathlib import Path

# def review_files(target_dir):
#     """
#     Every Markdown file in the vault.
#     """
#     for item in Path(target_dir).iterdir():
#         if item.is_file() and item.suffix == ".md":
#             new_file = ObsidianNote(item)
#             if "Web_Development" in new_file.tags and "Templates" not in str(item.parent):
#                 print(item.name)
#                 # new_file.tags.remove("Web_Development")
#                 # new_file.tags.append("Coding_and_Development/Web_Development")
#                 # new_file.write_file()
                
#         elif item.is_dir():
#             review_files(item)    


# review_files(vault)




my_file = Path(r"2022-09-07 Chest - Tricep_withFM.md")

new_file = ObsidianNote(my_file)

print(new_file.title)
print(new_file.created)
print(new_file.tags)




































