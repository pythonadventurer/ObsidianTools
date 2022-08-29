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
        self.categories = self.update_categories()

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
        key = topic id, value = topic description.
        '''
        topics_dict = {}
        for file in self.numbered_files:
            if file.counter == "000":
                topics_dict[file.topic_id] = file.title
                
        return topics_dict
        

    def update_categories(self):
        categories_dict = {}

        # create the categories dict
        for file in self.numbered_files:
            if file.topic_num == "00" and file.counter == "000":
                if file.category not in categories_dict:
                    categories_dict[file.category] = {"title":file.title}
                    categories_dict[file.category]["topics"] = []

        # go back over the files add the topic ids to each category
        for file in self.numbered_files:
            if file.category in categories_dict:
                if file.topic_num != "00" and file.topic_id not in categories_dict[file.category]["topics"]:
                    categories_dict[file.category]["topics"].append(file.topic_id)

        return categories_dict



    def topic_ids_by_category(self):
        '''
        list of topic IDs within each category.
        Used for assigning new topic IDs.
        '''
        pass


    def create_topic(self):
        while True:
            self.update_topics()
            topic_name = input("\nEnter a topic or <q> to go back: ")
            search_topics = [self.topics[topic].upper() for topic in self.topics.keys()]
            if topic_name.upper() in search_topics:
                new_topic_name = input(f"Sorry, topic '{topic_name}' already exists. Press <b> to enter another topic, or <q> to quit to the previous menu.")

                if new_topic_name[0].upper() == "Q":
                    return

                elif new_topic_name[0].upper() == "B":
                    continue

            elif topic_name.upper() == "Q":
                return

            else:
                action = input(f"Ready to create topic: '{topic_name}'? (Y/N) ")
                if action.upper() == "N":
                    continue
                else:
                    print("Topic creation not implemented.")
                    




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



