from Jack_Reader import Reader
from Tokenizer import Tokenizer
from Compilation import Compilation
import argparse
import glob
import os

class Parser:

    def __init__(self,file) -> None:
        self.dir = os.path.dirname(os.path.abspath(file))
        self.fname = os.path.basename(file)
        self.file = file

    def output_tokens(self,tokens):
        """outputs our xml file to the correct place"""
        if not os.path.isdir(self.dir+"/"+"analyzer"):
            os.mkdir(self.dir+"/"+"analyzer")
        
        output_path = self.dir +"/analyzer/" + self.fname[:-5] +"T.xml"

        with open(output_path,"w") as f:
            f.write("<tokens>\n")
            for token in tokens:
                tag = self.generate_tag(token[1])
                f.write(tag)
                f.write(token[0])
                tag = self.generate_tag(("/"+token[1]))
                f.write(tag)
                f.write("\n")
            f.write("</tokens>\n")

    def output_analyzer(self,instructions):
        """outputs our xml file to the correct place"""
        if not os.path.isdir(self.dir+"/"+"analyzer"):
            os.mkdir(self.dir+"/"+"analyzer")
        
        output_path = self.dir +"/analyzer/" + self.fname[:-5] +".xml"

        with open(output_path,"w") as f:
            for instruction in instructions:
                f.write(instruction)


    def generate_tag(self,tag):
        return f"<{tag}>"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts folder path")
    parser.add_argument('folder_path',type=str, metavar='folder_path', help="folder_path")  
    
    args = parser.parse_args()

    folder = args.folder_path
    folder_dir = os.path.abspath(folder) 

    jack_files = glob.glob(folder_dir+"/*.jack") #list of jack files
    

    for file_in in jack_files:
        reader = Reader(file_in)
        parser = Parser(file_in)
        clean_instructions = reader.clean_instructions()
        instructions = ''.join(clean_instructions)
        tokenizer = Tokenizer(instructions)
        tokenizer.get_all_tokens()
        parser.output_tokens(tokenizer.tokens)
        compiler = Compilation(tokenizer.tokens)
        compiler.compile_class()
        parser.output_analyzer(compiler.output)

