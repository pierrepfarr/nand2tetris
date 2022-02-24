## Project 8 VM Pt 2
<br>

### Overview
The following module turns VM code in Hack assembly code. The script accepts a directory with VM files ending in .vm and outputs an asm file ending in .asm in the same directory as the input. Code includes bootstrapping sys to start.

### Requirements
- python3
- input directory with .vm files
- The script makes use of the argparse, re, glob, and os modules from the python standard library 

### Usage

To run the file, navigate to the src directory and call python to execute the file along with one command line arguement with the absolute or relative path of the input file.

Absolute example:
```bash
$Home/src python3 VM_Translator.py root/desktop/input_dir/
```

Relative example:
```bash
$Home/src python3 VM_Translator.py ./input_dir/
```

## Results 

Successfully passed all test scripts provided. 