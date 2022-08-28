import re
from pathlib import Path

library_path = r"D:\Rob\Compendium\06_Library\DONE"
folder_name = r"C:\Users\robtf\Desktop\Compendium2\06.19_Politics"

def get_folder_list():
    for folder in Path(r"C:\Users\robtf\Desktop\Compendium2").iterdir():
        topic_id = folder.name[:5] + ".000"
        topic_file_name = topic_id + "_" + folder.name[6:] + ".md"
        topic_file = Path(folder,topic_file_name)
        topic_title = topic_file.stem[10:]
        with open(Path(folder,topic_file_name),"w") as f:
            f.write(f"""---\nfile_id: '{topic_id}'\ntype: 'topic'\ntitle: '{topic_title}'\n---""")
            f.write(f"\n# {topic_title}")

        
        print(topic_file_name)
        topicify_folders(folder,1)



def update_topic_files():
    """
    Add Dataview to topic files.
    """

    for file in Path(library_path).iterdir():
        if file.name[6:9] == "000":
            with open(file,"w") as f:
                title = file.stem.replace("_"," ")[10:]
                f.write(f"""---\nfile_id: '{file.name[:9]}'\ntype: 'topic'\ntitle: '{title}'\n---""")
                f.write(f"\n# {title}")


def topicify_folders(folder,counter_start):
    """
    Assign file IDs to files in topic folders.
    """
    counter = counter_start

    topic_id = Path(folder).name[:5]
    for file in Path(folder).iterdir():
        new_file_name = topic_id + f".{counter:0>3}_" + file.name
        print(new_file_name)
        file.rename(Path(folder_name,new_file_name))
 
        counter += 1




# topicify_folders(folder_name,1)

get_folder_list()
