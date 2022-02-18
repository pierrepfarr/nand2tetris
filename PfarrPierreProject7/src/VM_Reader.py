import argparse
import os

class Reader:

    
    def __init__(self,file):
        self.dir = os.path.dirname(os.path.abspath(file))
        self.fname = os.path.basename(file)
        self.file = file
        

    def clean_instructions(self):
        """cleans our vm file"""
        instructions = []
        lines = self.__read_file()
        for line in lines.splitlines():
            if line == "" or line == "\n":
                continue

            if line[:2] == "//":
                continue
            
            instructions.append(line)
        return instructions
    
    def __read_file(self)->str:
        try:
            with open(self.file) as f:
                lines = f.read()
            return lines
        except:
            print("Could not find the file")


    def output(self,instructions):
        """outputs our asm file to the correct place"""
        fname = self.fname[:-3]
        output_path = self.dir +"/" + fname +".asm"

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
    print(instrutions)