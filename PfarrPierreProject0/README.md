## Project 0 Programming Best Practices
<br>

### Overview
The following script removes white space and comments from a text file. The script accepts a text file ending in .in and outputs the cleaned file in the same directory as the input.

### Requirements
- python3
- input file ending in .in
- Comments may begin with a // and end at the return line
- Comments may begin /* and end with */
- All white space, tabs, and blank lines will be remove 
- The script makes use of the argparse, re, and os modules from the python standard library 

### Usage

To run the file, navigate to the src directory and call python to execute the file along with one command line arguement with the absolute or relative path of the input file.

Absolute example:
```bash
$Home/src python3 main.py root/desktop/input.in
```

Relative example:
```bash
$Home/src python3 main.py ./input.in
```