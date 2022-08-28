from pathlib import Path
import re

class ObsidianVault:
    def __init__(self,vault_folder):
        # TODO: allow vault_folder to be str or path
        self.vault_folder = Path(vault_folder)
        self.id_pattern = "^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]"
        self.numbered_files = []
        self.get_numbered_files(self.vault_folder)

    def get_numbered_files(self,folder):
        '''
        List of all numbered files in the vault.
        Each item in the list is a VaultFile class
        '''
        for item in folder.iterdir():
            if item.is_file():
                if re.match(self.id_pattern,item.name):
                    self.numbered_files.append(VaultFile(item))

            elif item.is_dir() and re.match(self.category_pattern,item.name):
                self.get_numbered_files(item)   

    def 


class VaultFile:
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.file_id = self.get_file_id()
        self.category = self.get_category()
        self.topic_num = self.get_topic_num()
        self.topic_id = self.get_topic_id()
        self.counter = self.get_counter() 
        self.file_name = self.file_path.name

        
    def get_file_id(self):
        file_id = self.file_path.name[:9]
        check_for_id = re.match("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]",file_id)
        if check_for_id != None:
            return check_for_id[0]
        else:
            return None
    
    def get_category(self):
        if self.file_id != None:
            return self.file_id[:2]
        else:
            return None

    def get_topic_num(self):
        if self.file_id != None:
           return self.file_id[3:5]
        else:
            return None

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
