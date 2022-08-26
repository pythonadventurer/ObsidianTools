from pathlib import Path
import re

class ObsidianVault:
    def __init__(self,vault_folder):
        # TODO: allow vault_folder to be str or path
        self.vault_folder = Path(vault_folder)
        self.category_pattern = "^[0-9][0-9]_"
        self.id_pattern = "^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]"
        self.get_category_folders()
        self.numbered_files = []
        self.get_numbered_files(self.vault_folder)
     
    def get_category_folders(self):
        '''
        List of category folders.
        '''
        self.category_folders = [item for item in self.vault_folder.iterdir() \
            if item.is_dir() and re.match(self.category_pattern,item.name)]

    def get_numbered_files(self,folder_path):
        '''
        List of all numbered files in a folder and its subfolder
        '''
        for item in folder_path.iterdir():
            if item.is_file():
                if re.match(self.id_pattern,item.name):
                    self.numbered_files.append(VaultFile(item))

            elif item.is_dir() and re.match(self.category_pattern,item.name):
                self.get_numbered_files(item)       

   
    
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

    