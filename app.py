from cgi import test
from lib import *

vault_folder = r"D:\Rob\Compendium"

test_file = r"D:\Rob\Compendium\06_Library\06.08.005_2002_10_17_Speed_and_Skill"

my_file = VaultFile(test_file)

print(my_file.file_id)
print(my_file.category)
print(my_file.topic_num)
print(my_file.counter)
print(my_file.topic_id)
print(my_file.next_topic_id)
print(my_file.next_counter)
























