import os
import argparse
import re

class White_Space():
    pattern_1 = re.compile("\/{2}.*$",re.MULTILINE)
    pattern_2 = re.compile("\/\*.*\*\/",re.DOTALL)

    def __init__(self,file):
        self.dir = os.path.dirname(os.path.abspath(file))
        self.fname = os.path.basename(file)
        self.file = file
        self.clean_file = None

    def clean(self):
        temp = self.__read_file()
        temp = re.sub(White_Space.pattern_1,"",temp) #remove comments
        temp = re.sub(White_Space.pattern_2,"",temp) #remove comments
        temp = temp.replace("\t","") #remove tabs
        temp = temp.replace(" ","") #remove spaces
        self.clean_file = temp

    def output(self):
        fname = self.fname[:-3]
        output_path = self.dir +"/" + fname +".out"

        with open(output_path,"w") as f:
            lines = self.clean_file.splitlines(True)
            for line in lines:
                if not line.isspace(): #making sure no blank lines make it out
                    f.write(line)

    def __read_file(self)->str:
        try:
            with open(self.file) as f:
                lines = f.read()
            return lines
        except:
            print("Could not find the file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")
    args = parser.parse_args()

    file_in = args.file_path
    file_out = White_Space(file_in)
    file_out.clean()
    file_out.output()