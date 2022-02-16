import argparse 
from whitespace import White_Space


class Assemble:
    """class attributes are command look-up tables"""
    
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
        self.symbols = {"SP":0,"LCL":1,"ARG":2,
                        "THIS":3,"THAT":4,"R0":0,
                        "R1":1,"R2":2,"R3":3,
                        "R4":4,"R5":5,"R6":6,
                        "R7":7,"R8":8,"R9":9,
                        "R10":10,"R11":11,"R12":12,
                        "R13":13,"R14":14,"R15":15,
                        "SCREEN":16384,"KBD":24576,}
        
        self.program_str = program_str
        self.var_mem = 16                               #variables start being store at 16   
        self.asm_instr = self.strip_labels(program_str) #clean asm instructions
        self.hack_instr = []                            #binary/hack instructions
        



    def strip_labels(self,program_str):
        """store and strip the labels and store variable symbols in look up"""
        self.store_labels(program_str)
        lines = []
        line_num = 0
        
        for line in program_str.splitlines()  :
            if not line.isspace() and len(line) != 0:
                if line.startswith("("):
                    continue
                
                elif line.startswith("@") and not line[1:].isdecimal():
                    symbol = line[1:]
                    if symbol not in self.symbols:
                        self.symbols[symbol] = self.var_mem
                        self.increment_var_mem()
                    lines.append(line)
                    line_num +=1
                
                else:
                    lines.append(line)
                    line_num +=1
        return lines

    
    def store_labels(self,program_str):
        """function to do a first pass and store the location of labels"""
        line_cnt = 0
        labels = 0    
        for line in program_str.splitlines():
            if not line.isspace() and len(line) != 0:
                if line.startswith("("):
                    symbol = line[1:-1]
                    if symbol not in self.symbols:
                        self.symbols[symbol] = (line_cnt-labels)
                        labels += 1
                line_cnt += 1


    def make_hack_instr(self):
        """go through each line and translate to binary"""
        for line in self.asm_instr:
            translated = self.translate_instruction(line)
            self.hack_instr.append(translated)
    
    
    def translate_instruction(self,instr):
        """depending on instr call correct logic"""
        if "=" in instr:
            hack_instr = self.c_instr_eq(instr)
        elif ";" in instr:
            hack_instr = self.c_instr_jmp(instr)
        elif "@" in instr:
            hack_instr = self.address(instr)
        return hack_instr

    
    def address(self,instr):
        """if an @ instructions then get decimal value and convert"""
        expression = instr.split("@")
        value = expression[1]
        if value.isdecimal():
            value = int(value)
            hack_instr = bin(value)[2:].zfill(16) #remove 0b base notation and pad to 16 digit
        else:
            value = self.symbols[value]
            hack_instr = bin(value)[2:].zfill(16)
        return hack_instr

    def c_instr_jmp(self,instr):
        """logic and lookups for jmp instructions"""
        expression = instr.split(";")
        left =  expression[0]
        right = expression[1]
        
        dest = self.destinations["Null"]
        comp = self.comp[left]
        jmp = self.jumps[right]
        
        hack_instr = "111"+comp+dest+jmp
        return hack_instr

        
    def c_instr_eq(self,instr):
        """logic and lookups for a computation instruction"""
        expression = instr.split("=")
        left = expression[0]
        right = expression[1]
        
        dest = self.check_left(left)
        comp = self.check_right(right)
        jmp = self.jumps["Null"]
        
        hack_instr = "111"+comp+dest+jmp
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

    
    def increment_var_mem(self):
        self.var_mem += 1
        # if self.var_mem > 32767:
        #     raise ValueError


    def output(self,dir,fname):
        fname = fname[:-4]
        output_path = dir +"/" + fname +".hack"

        with open(output_path,"w") as f:
            lines = self.hack_instr
            for line in lines:
                if not line.isspace() and len(line) != 0: #making sure no blank lines make it out
                    f.write(line+"\n")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file")
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    
    args = parser.parse_args()

    file_in = args.file_path
    
    input_file = White_Space(file_in)
    input_file.clean()
    
    assembler = Assemble(input_file.clean_file)
    assembler.make_hack_instr()
    assembler.output(input_file.dir,input_file.fname)

