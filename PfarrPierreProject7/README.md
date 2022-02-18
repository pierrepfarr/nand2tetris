## Project 7 VM Pt 1
<br>

### Overview
The following module turns VM code in Hack assembly code. The script accepts VM file ending in .vm and outputs an asm file ending in .asm in the same directory as the input.

### Requirements
- python3
- input file ending in .vm
- The script makes use of the argparse, re, and os modules from the python standard library 

### Usage

To run the file, navigate to the src directory and call python to execute the file along with one command line arguement with the absolute or relative path of the input file.

Absolute example:
```bash
$Home/src python3 VM_Translator.py root/desktop/input.VM
```

Relative example:
```bash
$Home/src python3 VM_Translator.py ./input.vm
```

## Results 

Successfully passed all test scripts provided.