# Organizing Everything

Insipired by https://johnnydecimal.com/.


Goal: Organize a huge number of files using only a system of file naming. 

However, the file naming system is designed so that a folder system can be created via code, using the file naming system itself as a specification.

## Features
- Even a single folder with a huge number of files will have a naming system that will cause the files to sort in a way that makes sense to the user.
- Code can be used to organize the files into a folder structure based on the file naming system.  Conversely, code can also be used to extract those same files from the folder structure and place them all back in a single folder.  This ensures maximum portability between apps and filing systems.

## Use Cases
- Obsidian note taking app.  One of this app's greatest strengths is that it automatically indexes all files in a vault, regardless of folder structure, and makes every file available to link to from any note. You can have a folder structure that bears no resemblance whatsoever to your system of file linking, and even move files around between folders and sub folders, and Obsidian automatically updates links.  This means you can change your Obsidian folder structure on the fly, and links won't break.
- Everyday file and folder organization on a PC.  The beauty of this system is that it workes on any computer, with just the operating system's built-in file explorer and text editor.  No specialized application is required.

## System Specifiations

### File ID
- Every file is assigned an ID number in the format 00.00.000.  This ID is always at the beginning of the file and separated from the rest of the file name by an underscore.  Example:

    02.04.006_My_Awesome_File.pdf

The parts of the file ID are:

02 : Category.  Denotes the general type of the file.  Examples: Work, Personal, Journal, Projects, Sales, Finance, etc.

04 : Topic.  Should be as specific as possible, easy to remember, and helpful when browsing the file system. Examples: 

006 : Counter.  Unique ID, within the topic, to idenfity the file

The rest of the file after the first underscore should be a useful description of the file.

Text files are used as "headings" for a topic and always have counter number "000". Example:

    02.04.000_Awesome_Files.md

Within a folder, these will always sort to the beginning of the set of files with the same category and topic.

### File Naming Specifications

- File names may only consist of numbers, letters and underscores.  No spaces, dashes, commas, apostrophes or special characters.  Commas and spaces are to be replaced by underscores, and apostrophes removed.  Periods are only allowed in the file ID and to denote the file extension.


