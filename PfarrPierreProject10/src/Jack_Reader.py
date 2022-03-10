import argparse
import os
import re

class Reader:

    pattern_1 = re.compile("\/{2}.*$",re.MULTILINE)
    pattern_2 = re.compile("\/\*.*?\*\/",re.DOTALL)

    def __init__(self,file):
        self.dir = os.path.dirname(os.path.abspath(file))
        self.fname = os.path.basename(file)
        self.file = file



    def clean_instructions(self):
        """cleans our jack file"""
        instructions = []

        temp = self.__read_file()
        temp = re.sub(Reader.pattern_1,"",temp) #remove comments
        temp = re.sub(Reader.pattern_2,"",temp) #remove comments
        for line in temp.splitlines():
            if line == "" or line == "\n":
                continue
            instructions.append(line.strip())
        return instructions


    def __read_file(self)->str:
        try:
            with open(self.file) as f:
                lines = f.read()
            return lines
        except:
            print("Could not find the file")


    def output(self,instructions):
        """outputs our xml file to the correct place"""
        fname = os.path.basename(self.dir)
        output_path = self.dir +"/" + fname +".xml"

        with open(output_path,"w") as f:
            for line in instructions:
                if not line.isspace() and len(line) != 0: #making sure no blank lines make it out
                    f.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    
    args = parser.parse_args()

    file_in = args.file_path
    file_out = Reader(file_in)
    instrutions = file_out.clean_instructions()
    instrutions = ''.join(instrutions)
    print(instrutions)