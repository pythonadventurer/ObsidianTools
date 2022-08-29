from pathlib import Path
import re
import sys


class ObsidianVault:
    def __init__(self,vault_folder):
        self.vault_folder = Path(vault_folder)
        self.id_pattern = "^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]"
        self.numbered_files = []
        self.get_numbered_files(self.vault_folder)
        self.topics = self.update_topics()

    def get_numbered_files(self,folder):
        '''
        List of all numbered files in the vault.
        Each item in the list is a VaultFile class
        '''
        for item in folder.iterdir():
            if item.is_file():
                if re.match(self.id_pattern,item.name):
                    self.numbered_files.append(VaultFile(item))

            elif item.is_dir():
                self.get_numbered_files(item)   

    def update_topics(self):
        '''
        List of all topic IDs (NN.NN)
        '''
        topics_dict = {}
        for file in self.numbered_files:
            if file.counter == "000":
                topics_dict[file.topic_id] = file.title
                
        return topics_dict


class VaultFile:
    '''
    file_id = filename[:9]
    topic_id = filename[:5]
    category_id = filename[0:2]
    topic_num = filename[3:5]
    counter = file_id[-3]
    file_name = filename[10:]

    '''
    def __init__(self,file_path):
        self.file_path = Path(file_path)
        self.file_id = self.get_file_id()
        self.category = self.get_category()
        self.topic_num = self.get_topic_num()
        self.topic_id = self.get_topic_id()
        self.counter = self.get_counter() 
        self.file_name = self.file_path.name
        self.title = self.file_path.stem[10:].replace("_"," ")

        
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
            return self.file_id[:5]

        else:
            return None

    def get_counter(self):
        if self.file_id != None:
            return self.file_id[6:]
        else:
            return None

def process_files(folder):
    """
    Categorize and add files to an Obsidian vault.
    """

    file_menu = """
    <t> Assign topic; <s> Skip to next file; q> Quit

    Please select an option: """

    for file in Path(folder).iterdir():
        print(f"\nCurrent file: {file.name}")
        while True:
            response = input(file_menu)
            if response[0].upper() == "Q":
                print("Goodbye!")
                sys.exit()

            elif response[0].upper() == "S":
                break


def create_topic(topic_name,vault_obj):
    while True:
        for topic in vault_obj.topics.keys():
            if topic_name == vault_obj.topics[topic]:
                new_topic_name = input("Sorry, topic '{topic_name} already exists. Press <b> to enter another topic, <c> to create the new topic, or <q> to quit to the previous menu.")

                if new_topic_name[0].upper() == "Q":
                    return None

                elif new_topic_name[0].upper() == "B":
                    
