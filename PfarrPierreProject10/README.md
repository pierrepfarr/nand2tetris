## Project 10 Syntax Analyzer
<br>

### Overview
The following module parses Jack code into XML. The script accepts a directory with Jack files ending in .jack and outputs corresponding files ending in .xml in the same parent directory but under a new folder called analyzer (this was done because the supplied test files had matching names).

### Requirements
- python3
- input directory with .jack files
- The script makes use of the argparse, re, glob, and os modules from the python standard library 

### Usage

To run the file, navigate to the src directory and call python to execute the file along with one command line arguement with the absolute or relative path of the input file.

Absolute example:
```bash
$Home/src python3 Analyzer.py root/desktop/input_dir/
```

Relative example:
```bash
$Home/src python3 Analyzer.py ./input_dir/
```

## Results 

Successfully compared againist the recommended files.