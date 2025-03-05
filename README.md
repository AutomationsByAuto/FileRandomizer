# File Randomizer

A Python tool designed to randomize filenames within a directory by renaming files with numbered prefixes (e.g., `_1filename.txt`), with a reversible process tracked via CSV. Ideal for automation tasks requiring file organization.  
Includes an executable in [Releases](https://github.com/AutomationsByAuto/FileRandomizer/releases) for easy usablilty.   
Remember to "sort by name" in Windows for effective (and fastest) results.   
Be patient with the initial use of the `.exe`  
Following this it will run normally.   

## Features
- Randomly prefixes filenames with numbers (e.g., `_1`, `_2`).
- Reverses changes using a CSV tracker (`DO_NOT_DELETE_all_file_names.csv`).
- Removes prefixes and recreates the CSV if missing.
- Updates CSV with new or deleted files dynamically.
- Portable: Includes a standalone `.exe` for Windows users.

## Installation
### For Python Users
1. Clone the repository:
   ```bash
   git clone https://github.com/AutomationsByAuto/FileRandomizer.git
   cd FileRandomizer

### Note:   
If you decide to build this into an `.exe` the csv created by this script will be required.  
Make sure you run the script once before building. 

### For Executable Users
- Download `file_randomizer.exe` from the [Releases](https://github.com/AutomationsByAuto/FileRandomizer/releases) section.
- Place it in the directory with files to randomize and double-click to run.
- The initial run will be slow to open.
- Following this the program will start much faster. 

## Motivation
I found I was unable to organise a directory of images and videos randomly in Windows so I coded this solution.  

Built as my first step into automation engineering, this tool demonstrates file manipulation, user interaction, and portability—core skills for automating repetitive tasks.

## License
MIT License - feel free to use, modify, and distribute.

## Contact
Ray Pitcher - mass.automation.solutions@gmail.com

Aspiring Automation Engineer | Open to feedback and collaboration!
