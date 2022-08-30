from hashlib import new
from pathlib import Path
import re
import sys
import os


class ObsidianVault:
    def __init__(self,vault_folder):
        self.vault_folder = Path(vault_folder)
        self.id_pattern = "^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]"
        self.numbered_files = []
        self.get_numbered_files(self.vault_folder)
        self.topics = self.update_topics()
        self.categories = self.update_categories()
        self.file_heading = "---\nfile_id: '{}'\ntype: '{}'\ntitle: '{}'\n" + \
                            "---\n# {}"

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
                topics_dict[file.topic_id] = {"title":file.title}
                topics_dict[file.topic_id]["counters"] = []
        # get counters
        for file in self.numbered_files:
            if file.topic_id in topics_dict:
                topics_dict[file.topic_id]["counters"].append(file.counter)

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

    def create_topic(self, topic_name):
        while True:
            self.update_topics()
                
            # search for topic by name
            search_topics = [self.topics[topic]["title"].upper() for topic in self.topics.keys()]
            if topic_name.upper() in search_topics:
                new_topic_name = input(f"Sorry, topic '{topic_name}' already exists. Please enter another topic, or <q> to quit to the previous menu.")

                if new_topic_name[0].upper() == "Q":
                    return

                elif new_topic_name[0].upper() == "B":
                    self.create_topic(new_topic_name)

            elif topic_name.upper() == "Q":
                return

            else:
                action = input(f"Ready to create topic: '{topic_name}'? (Y/N) ")
                if action.upper() == "N":
                    return

                else:
                    # default category to Library. 
                    # TODO Add category selection option.
                    new_topic_category = "06"
                    max_topic_id = max(self.categories[new_topic_category]["topics"])[-2:]
                    new_topic_id = new_topic_category + "." + f"{int(max_topic_id) + 1:0>2}" + ".000"
                    new_topic_name = new_topic_id + "_" + topic_name.replace(" ","_") + ".md"
                    new_topic_path = Path(self.vault_folder, r"06_Library",new_topic_name)
                    with open(new_topic_path,"w") as f:
                        f.write(self.file_heading.format(new_topic_id,"topic",topic_name,topic_name))
                    print(f"Topic: '{new_topic_name} created.")
                    self.update_topics()   
                    return               

    def assign_topic(self,file, topic_id):
        # search for topic by topic_id
        if topic_id in self.topics.keys():
            new_counter = int(max(self.topics[topic_id]["counters"])) + 1
            new_counter = f"{new_counter:0>3}"
            new_file_name = topic_id + "." + new_counter + "_" + file.name 
            new_file_path = Path(self.vault_folder,"06_Library",new_file_name)
            file.rename(new_file_path)
            print(f"New file: '{new_file_path}' added.")

        else:
            print("Topic ID does not exist.")
        
        return

    def process_files(self,folder):
        """
        Categorize and add files to an Obsidian vault.
        """
        file_menu = """
        <t> Assign topic; <s> Skip to next file; <v> View file; <c> Create topic; q> Quit

        Please select an option: """

        for file in Path(folder).iterdir():
             print(f"\nCurrent file: {file.name}")
             while True:
                response = input(file_menu)
                if response[0].upper() == "Q":
                    print("Goodbye!")
                    sys.exit()

                elif response[0].upper() == "S":
                    # break out of the 'while' loop and go back to the top of the 'for' loop
                    break

                elif response[0].upper() == "V":
                    os.startfile(file)

                elif response[0].upper() == "C":
                    new_topic = input("Enter a topic: ")
                    self.create_topic(new_topic)

                elif response[0].upper() == "T":
                    assign_topic = input("Enter topic ID (NN.NN): ")
                    self.assign_topic(file,assign_topic)
                    break
                
                elif re.match("^[0-9][0-9]",response):
                    # if response is a valid topic ID, go straight to assign topic
                    self.assign_topic(file, response)
                    break








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
