## Project 6 Assembler
<br>

### Overview
The following module turns assembly language into binary. The script accepts an asm file ending in .asm and outputs a hack file ending in .hack in the same directory as the input.

### Requirements
- python3
- input file ending in .asm
- The script makes use of the argparse, re, and os modules from the python standard library 

### Usage

To run the file, navigate to the src directory and call python to execute the file along with one command line arguement with the absolute or relative path of the input file.

Absolute example:
```bash
$Home/src python3 main.py root/desktop/input.asm
```

Relative example:
```bash
$Home/src python3 main.py ./input.asm
```

## Results 

Successfully compared by running pong and example files. Also by comparing output to output from the nand2tetris given assembler.