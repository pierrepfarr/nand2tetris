import argparse 
from whitespace import White_Space


class Assemble:

    destinations = {"Null":"000","M":"001","D":"010",
                    "A":"100","MD":"011","DM":"011",
                    "MA":"101","AM":"101","DA":"110",
                    "AD":"110","AMD":"111","ADM":"111",
                    "MAD":"111","MDA":"111","DAM":"111",
                    "DMA":"111","MDA":"111"}

    jumps =        {"Null":"000","JGT":"001","JEQ":"010",
                    "JGE":"011","JLT":"100","JNE":"101",
                    "JLE":"110","JMP":"111"}

    comp =         {"0":"0101010","1":"0111111","-1":"0111010",
                    "D":"0001100","A":"0110000","!D":"0001101",
                    "!A":"0110001","-D":"0001111","-A":"0110011",
                    "D+1":"0011111","A+1":"0110111","D-1":"0001110",
                    "A-1":"0110010","D+A":"0000010","D-A":"0010011",
                    "A-D":"0000111","D&A":"0000000","D|A":"0010101",
                    "M":"1110000","!M":"1110001","-M":"1110011",
                    "M+1":"1110111","M-1":"1110010","D+M":"1000010",
                    "D-M":"1010011","M-D":"1000111","D&M":"1000000",
                    "D|M":"1010101"}

    def __init__(self,program_str):
        self.symbols = {}
        self.asm_instr = self.strip_labels(program_str)
        self.hack_instr = []


    def strip_labels(self,program_str):
        """strip the labels out of the program and put in table"""
        pass


    
    def c_instr(self):
        """generate a c instr"""
    
    def check_left(self):
        """look up the left side of ="""
        pass

    def check_right(self):
        """look up the right side of ="""
        pass

    









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    # accept a postional arguement for the file path
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    args = parser.parse_args()

    file_in = args.file_path
    file_out = White_Space(file_in)
    file_out.clean()
 