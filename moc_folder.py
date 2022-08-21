from pathlib import Path

vault = Path(r"D:/Rob/InfoCenter")
moc_folder = r"Topics/United_States"


def moc(moc_folder):
    '''
    vault_folder : a Path object.  The complete path to the Obsidan vault folder.
        Example: Path(r"D:/Rob/InfoCenter")

    moc_folder : the path of the folder whose content is to be mapped, relative to
    vault_folder.
        Example: r"Topics/United_States"


    Create a Map of Content (MOC) of all files in the selected folder.

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
    # Absolute path to MOC folder
    vault_moc = Path(vault, moc_folder)

    for item in vault_moc.iterdir():
        if item.is_file() and item.suffix != "md":
            meta_file_path = Path(vault_moc,item.stem + ".md")
            meta_file_title = item.stem.replace("_"," ")
            meta_file_link_path = "[[" + moc_folder + "/" + item.name + "|" + meta_file_title + "]]"

            with open(meta_file_path,"w",encoding="utf-8") as meta_file:
                meta_file.write("# " + meta_file_title + "\n\n")
                meta_file.write(meta_file_link_path + "\n")    

            print(str(meta_file_title))
            print(str(meta_file_path))
        elif item.is_dir():
            moc(item)

            
    # Create an index page, with links to all the metadata pages.
    # Page will have the same name as moc_folder, plus ".md"
    moc_index_file_path = Path(vault_moc, "_MOC_Index_" + vault_moc.name + ".md")
    moc_index_file_title = "# " + vault_moc.name.replace("_"," ") + "\n\n"
    with open(moc_index_file_path,"w",encoding = 'utf-8') as index_file:
        index_file.write(moc_index_file_title)    
        for item in vault_moc.iterdir():
            if item.suffix == ".md" and item != moc_index_file_path:
                link_path = "[[" + moc_folder + "/" + item.stem + ".md" + "|" + item.stem.replace("_"," ") + "]]\n"
                index_file.write(link_path)



