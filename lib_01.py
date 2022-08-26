from pathlib import Path
import re
import sys

def map_content(vault_folder, moc_folder_rel):
    '''   
    Create a Map of Content (MOC) of all files in the selected folder.
    vault_folder : String. The absolute path to the Obsidian vault

    moc_folder : String. Path of the folder to be mapped, relative to vault_folder

    Each document will have a corresponding Markdown file, with information about the file, such as 
    text excepts, source URL,thoughts and response, why it's important, etc.  It's basically
    metadata about the file.  
        - This markdown file will contain a link to the document it pertains to, and
    will reside in the same folder as the socument.
        - The markdown file name will be the same as the document file name, with the extension ".md".
        - The title in this markdown file will be the same as the markdown file name, less ".md", and
        with underscores replaced by spaces.

    Create a page in obsidian_folder with same name as the folder, with the prefix "_Index_" and
    suffix ".md"
        - Page title: page name with underscores replaced with spaces.
        - Resides in same folder as the topic files, and the corresponding Markdown files.
        - Links to all the "metadata" Markdown files.
    '''  
    moc_folder_abs = Path(vault_folder, moc_folder_rel)
    print(f"Mapping content in folder: {moc_folder_rel}")
    for item in moc_folder_abs.iterdir():
        # Create "metadata" Markdown pages for each item.
        # Existing Markdown files are kept as-is. Meta files are only for
        # non Markdown docs.
        if item.is_file() and item.suffix != "md":

            # Since we're creating the metadata file outside Obisidian, we need
            # to use the absolute path in creating the new md file.
            meta_file_path = Path(moc_folder_abs, item.stem + ".md")

            # Do not overwite existing metadata files!
            if meta_file_path.exists() == False:
                meta_file_title = item.stem.replace("_"," ")
                
                # The link to be created within the metadata file that will point to the item.         
                # Links within the Obsidian vault are relative to the vault folder.
                meta_file_link_path = "[[" + str(Path.as_posix(Path(moc_folder_rel,item.name))) + "|" + meta_file_title + "]]"

                with open(meta_file_path,"w",encoding="utf-8") as meta_file:
                    meta_file.write("# " + meta_file_title + "\n\n")
                    meta_file.write(meta_file_link_path + "\n")    
                    print(f"Created meta file: {str(meta_file_path)}")

        elif item.is_dir():
            moc_subdir_rel = str(Path.as_posix(Path(moc_folder_rel,item.name)))
            map_content(vault_folder, moc_subdir_rel)

    # Create an index page, with links to all the metadata pages.
    # Page will have the same name as moc_folder, plus ".md"
    moc_index_file_path = Path(moc_folder_abs, "_Index_" + moc_folder_abs.name + ".md")
    moc_index_file_title = "# " + moc_folder_abs.name.replace("_"," ") + "\n\n"
    with open(moc_index_file_path,"w",encoding = 'utf-8') as index_file:
        index_file.write(moc_index_file_title)    
        for item in moc_folder_abs.iterdir():
            if item.suffix == ".md" and item != moc_index_file_path:
                link_path = "[[" + moc_folder_rel + "/" + item.stem + ".md" + "|" + item.stem.replace("_"," ") + "]]\n"
                index_file.write(link_path)

    print(f"Created index file: {moc_index_file_path}")

def table_of_contents(folder):
    '''
    folder : string
    Iterate over a folder and its subfolders.  Find Markdown files whose name 
    starts with with "_Index_" and create a hierarchial Table of Contents from them, with links
    to each file.
    '''
    for item in Path(folder).iterdir():
        if item.is_dir():
            for file in item.iterdir():
                print(file.name[:11])


def find_indexes(folder):
    '''
    Iterate recursively over items in folder and find '_MOC_Index_' files.
    '''
    for item in Path(folder).iterdir():
        if item.is_file():
            if item.name[:11] == "_MOC_Index_":
                print(item.name)
                item.rename(item.name[4:])

        else:
            find_indexes(str(item))
            
       

def eliminate_dashes(document_folder):
    for file in Path(document_folder).iterdir():
        if "-" in file.name:
            new_name = str(file).replace("-","_")
            # file.rename(Path(new_name))
            # print(new_name)
            print(file.name)

 

class FilingAssistant:   
    '''
    Assign numeric IDs to documents based on the Indexing System.
    Lists each un-numbered file for user input.
    Options:
    - List existing topics by ID and name
    - Enter a topic ID <00.00>
        - If missing, ask to create
            - Prompt for topic name
            - Create topic placeholder md file
        - Display new file name, with topic ID and counter
            number, and confirm rename
    - List files by topic ID <00.00>
    - Quit
    '''

    def __init__(self,document_folder):
        self.document_folder = document_folder
        self.update_file_lists()
        self.categories = {"Index":"00",
                           "Inbox":"01",
                           "Projects":"02",
                           "Journal":"03",
                           "Personal":"04",
                           "Bible_Study":"05",
                           "Library":"06"}
    

    def update_file_lists(self):

        # update all file lists.
        self.get_file_list()
        self.get_topics()
        self.get_topics_alpha()
        self.get_topic_ids()
        self.get_items_to_file()
        self.get_numbered_files()
        self.get_max_nums()


    def get_file_list(self):
        # All files in folder.
        self.file_list = [file.name for file in Path(self.document_folder).iterdir()]
    
    def get_topics(self):
        # Topic placeholder files
        self.topics = [file for file in self.file_list if file[6:9] == "000"]
    
    def get_topics_alpha(self):
        # Topics listed alphabetically.
        topics_list = self.topics
        split_topics = [[file[:file.find("_")],file[file.find("_")+1:]] for file in topics_list]
        topics_dict = {}
        for topic in split_topics:
            topics_dict[topic[1][:len(topic[1])-3]] = topic[0]
        topics_alpha = sorted(topics_dict)
        self.topics_alpha = [topics_dict[topic] + " " + topic for topic in topics_alpha]

    def get_topic_ids(self):
        # Topic category & number prefixes (e.g. 06.02)
        self.topic_ids = [num[:5] for num in self.topics]

    def get_items_to_file(self):
        # Files that have not been given an ID.
        self.to_file = []      
        for file in self.file_list:
            match = re.match("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]_",file)
            if match == None:
                self.to_file.append(file)

    def get_numbered_files(self):
        # Files that have been given an ID.
        self.numbered_files = [file for file in self.file_list if re.match("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9]_",file)]

    def get_max_nums(self):
        # Dictionary of the last counter number issued for each topic.
        self.get_numbered_files
        self.max_nums = {}
        for topic_id in self.topic_ids:
            nums_list = [file for file in self.numbered_files if file[:5] == topic_id]
            self.max_nums[topic_id] = max(nums_list)[6:9]

    def list_items(self,file_list):
        # Print a list of items.
        p = [print(item) for item in file_list]
       

    def list_files_by_topic(self, topic_id):
        '''
        List of files with the given topic ID.
        '''
        self.get_numbered_files()
        for file in self.numbered_files:
            if file[:5] == topic_id:
                print(file)

# TODO Deal with specifying categories and finding last assigned topic ID for a category.
    def create_topic(self):
        self.get_topics()
        last_topic_id = max(self.topic_ids)
        print("Last topic ID: " + last_topic_id)
        topic_name = input("Enter topic name: ").replace(" ","_")
        new_topic_id = "06." + f"{int(last_topic_id[3:5]) + 1:0>2}"
        topic_file = Path(self.document_folder,new_topic_id + ".000_" + topic_name + ".md")
        with open(topic_file,"w",encoding = "utf-8") as f:
            f.write("\n")
        print("Topic created: " + str(topic_file))

    def process_files(self):
        '''
        Interactive process for assigning IDs to files.
        # >>> i = 1
        # >>> f"{i:0>2}"  # Works for both numbers and strings.
        '''
        self.get_items_to_file()
        for file in self.to_file:
            while True:
                print(f"Current file: {file}")
                response = input("\n<a>ssign ID, <l>ist topics, <c>create topic, <n>ext file, <q>uit: ")
                if response.upper() == "Q":
                    print("Bye!")
                    sys.exit()
                
                elif response.upper() == "A":
                    self.get_topic_ids()
                    topic_id = input("Enter a topic ID (NN.NN): ")
                    if topic_id not in self.topic_ids:
                        r = input("Topic does not exist. Create? (Y/N): ")
                        if r.upper() == "Y":
                            self.create_topic()
                            break
                        else:
                            break
                    else:
                        self.get_max_nums()
                        new_counter = int(self.max_nums[topic_id]) + 1
                        new_file_name = topic_id + "." + f"{new_counter:0>3}" + "_" + file
                        new_file_path = Path(Path(self.document_folder),new_file_name)
                        old_file_path = Path(Path(self.document_folder),file)
                        old_file_path.rename(new_file_path)    
                        print(f"Renamed to: {new_file_name}")        
                        break

                elif response.upper() == "L":
                    self.get_topics()
                    self.get_topics_alpha()
                    file_list = self.topics_alpha
                    self.list_items(file_list)
                    with open(Path(self.document_folder,""),"w",encoding = "utf-8") as f:
                        f.write("\n")

                
                elif response.upper() == "N":
                    break
                
                elif response.upper() == "C":
                    self.create_topic()

                else:
                    print("Invalid response.")

