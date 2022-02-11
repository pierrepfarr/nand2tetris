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
        lines = program_str.splitlines()
        return lines

    def make_hack_instr(self):
        for line in self.asm_instr:
            translated = self.translate_instruction(line)
            self.hack_instr.append(translated)
    
    def translate_instruction(self,instr):
        hack_instr=""
        if "=" in instr:
            hack_instr = self.c_instr_eq(instr)
        elif ";" in instr:
            hack_instr = ""
        elif "@" in instr:
            hack_instr = ""
        return hack_instr

    def c_instr_eq(self,instr):
        """translate a c instr"""
        expression = instr.split("=")
        left = expression[0]
        right = expression[1]
        dest = self.check_left(left)
        comp = self.check_right(right)
        hack_instr = "111"+comp+dest+"000"
        return hack_instr

    def check_left(self,left_hand):
        """look up the left side of ="""
        if left_hand in self.destinations:
            return self.destinations[left_hand]
        else:
            return self.destinations["Null"]

    def check_right(self,right_hand):
        """look up the right side of ="""
        return self.comp[right_hand]

    









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    # accept a postional arguement for the file path
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    args = parser.parse_args()

    file_in = args.file_path
    file_out = White_Space(file_in)
    file_out.clean()
    translated = Assemble(file_out.clean_file)
    translated.make_hack_instr()

