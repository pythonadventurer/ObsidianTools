from pathlib import Path


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

    Create a page in obsidian_folder with same name as the folder, with the prefix "MOC_" and
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
    moc_index_file_path = Path(moc_folder_abs, "_MOC_Index_" + moc_folder_abs.name + ".md")
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
    starts with with "_MOC_Index" and create a hierarchial Table of Contents from them, with links
    to each file.
    '''
    for item in Path(folder).iterdir():
        if item.is_dir():
            for file in item.iterdir():
                print(file.name[:11])

