# Obsidian Tools :  Miscellaneous Python tools for the Obsidian note taking app.

## Description

A set of tools to help organize files in [Obsidian](https://obsidian.md).

## Warning : Here Be Dragons

**THIS IS A WORK IN PROGRESS.  DOCUMENTATION MAY BE SPARSE OR NON-EXISTENT.**

## Copyright and License

Obsidian Tools is an open-source program. This means it can be used and distributed freely under the conditions of the license.

All files in this package, unless otherwise noted, are copyrighted by Robert T. Fowler IV <robtf04@outlook.com>

## Filing System

Inspired by [Johnny Decimal](https://johnnydecimal.com).

These tools are designed to work with a specific file organizational structure, described herein.
### Goals
- Organize a huge number of files using only a system of file numbering.  
- Provide the minimum structure needed in order to find a file easily via browsing.
- Consistency, so that the system can be incorporated into a file organizing application.
- Portability and platform independence.

### Features
- Numbering system is platform-independent.
- Even a single folder with a huge number of files will have a numbering system that will cause the files to sort in a way that makes sense to the user.
- A document's subject matter can be known regardless of its location in the file system.
- Code can be used to organize the files into a folder structure based on the file naming system.  Conversely, code can also be used to extract those same files from the folder structure and place them all back in a single folder.  This ensures maximum portability between apps and filing systems.

### Use Cases
- Primarily designed to work with the [Obsidian](https://obsidian.md) note taking app and some [Python](https://www.python.org) scripts to help name and organize files.  One of this app's greatest strengths is that it automatically indexes all files in a vault, regardless of folder structure, and makes every file available to link to from any note. You can have a folder structure that bears no resemblance whatsoever to your system of file linking, and even move files around between folders and sub folders, and Obsidian automatically updates links.  This means you can change your Obsidian folder structure on the fly, and links won't break.
- File and folder organization on a computer.  The beauty of this system is that it works on any computer, with just the operating system's built-in file explorer and text editor.  No specialized application is required.

### Challenges
- System easily becomes cumbersome to manage manually.  As the number of files increases, it becomes more difficult to keep track of category and topic numbers. 

### System Specifications
#### File Types
- System can be used to organize almost any collection of files whose name can be changed.  This excludes system files or files required by specific applications that are not designed to be altered by any program other than the indended program.
- All text files are to be in Markdown format and have the extension "*.md".
  
#### File ID
- Every file is assigned an ID number in the format 00.00.000.  This ID is always at the beginning of the file and separated from the rest of the file name by an underscore.  Example:

    02.01.001_An_Awesome_File.pdf

The parts of this example file ID are:

    02 : Category.  Denotes the general type of the file.  Examples: Work, Personal, Journal, Projects, Sales, Finance, etc.
    01 : Topic.  Should be as specific as possible, easy to remember, and helpful when browsing the file system. Examples: 
    001 : Counter.  Unique ID, within the topic, to identify the file

The rest of the file after the first underscore should be a useful description of the file.

Text files are used as "headings" for categories and topics, and always have counter number "000". Example:

    02.04.000_Awesome_Files.md

A heading for a Category file will have topic 00 and counter 000.  Example:

    02.00.00_Filing_Cabinet

#### Summary

- Example filing system: a folder containing the following files:

gi```
    02.00.000_Filing_Cabinet.md                    --> This file specifies a category, which in this case is numbered '02.
    02.01.000_My_Awesome_Files.md                  --> This file specifies a topic within a category.
    02.01.001_An_Awesome_File.pdf                  --> A file with a category and topic
    02.01.002_Another_Really_Great_File.pdf        --> A file with a category and topic
    02.02.000_Homework.md                          --> Another topic in the category 'Filing Cabinet." 
    02.02.001_Notes_for_Final_Exam.pdf
    02.02.002_When_Homework_Becomes_Dog_Food.pdf
```

- This numbering system ensures that the files in a folder will always sort neatly by category and topic.

#### File Naming Specifications
- File names may only consist of numbers, letters and underscores. 
- No spaces, dashes, commas, apostrophes or special characters.  
- Commas and spaces are to be replaced by underscores, and apostrophes removed.  Periods are only allowed in the file ID and to denote the file extension.
  
