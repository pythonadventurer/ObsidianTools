from pathlib import Path
import re

class ObsidianVault:
    def __init__(self,vault_folder):
        self.vault_folder = vault_folder
        self.categories = self.get_categories()
    

    def get_categories(self):
        '''
        Get categories from the top level folder structure.
        Folder name format: NN_Folder_Name required to be recognized
        as a category.

            NN : Category ID (00 - 99)
            Folder Name : Must be letters, numbers and underscores ONLY. 
        '''
        self.categories = {}
        for item in Path(self.vault_folder).iterdir():
            pass

    def get_topic_ids(self, file_list, category_id):
        '''
        Files within a folder have that folder's category ID, plus
        a two-digit topic ID, plus a counter. Example:
            NN.NN.NNN_File_Description.ext
        This function extracts the two digit topic ID from file names
        with the given category ID.
        '''
        pass

    def get_file_names(self,folder):
        '''
        Get a list of all files in a folder.
        '''
        pass
    
    def get_counters(self,category_id, topic_id,folder):
        '''
        Extracts the three digit counter from file names with the 
        given category + topic id.
        '''
        pass

    def new_topic(self,category_id, folder):
        '''
        Creates a new topic id file
        '''
    
class VaultFile:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.get_file_id()
        self.get_category()
        self.get_topic_num()
        self.get_topic_id()
        self.get_counter() 
        self.get_next_topic_id()
        self.get_next_counter()


    def get_file_id(self):
        file_id = self.file_path.name[:9]
        check_for_id = re.match("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]",file_id)
        if check_for_id != None:
            self.file_id = check_for_id[0]
        else:
            self.file_id = None
    
    def get_category(self):
        if self.file_id != None:
            self.category = self.file_id[:2]
        else:
            self.category = None

    def get_topic_num(self):
        if self.file_id != None:
            self.topic_num = self.file_id[3:5]
        else:
            self.topic_num = None

    def get_topic_id(self):
        if self.file_id != None:
            self.topic_id = self.file_id[:5]
        else:
            self.topic_id = None
            
    def get_counter(self):
        if self.file_id != None:
            self.counter = self.file_id[-3:]
        else:
            self.counter = None

    def get_next_topic_id(self):
        if self.file_id != None:
            self.next_topic_id = self.category + "." + f"{int(self.topic_num) + 1:0>2}"
        else:
            self.next_topic_id = None

    def get_next_counter(self):
        if self.file_id != None:
            self.next_counter = f"{int(self.counter) + 1:0>3}"
        else: 
            self.next_counter = None

    