from VM_Reader import Reader
from Arithmetic import Stack_Arithmetic
from Memory_Access import Memory_Access

import argparse


class Translator:

    def __init__(self,instructions):
        self.vm_instructions = instructions
        self.asm_instructions = []
        self.label_cnt = 0

    def translate(self):
        """check for vm instruction and translate storing to asm_instr list"""
        for instruction in self.vm_instructions:
            print(instruction)
            if "push" in instruction or "pop" in instruction:
                mem_instr = Memory_Access(instruction)
                mem_instr.translate()
                for instr in mem_instr.asm_instructions:
                    self.asm_instructions.append(instr)
            else:
                arithmetic_instr = Stack_Arithmetic(instruction,self.label_cnt)
                arithmetic_instr.translate()
                for instr in arithmetic_instr.asm_instructions:
                    self.asm_instructions.append(instr)
                if instruction in ["lt","gt","eq"]:
                    self.increment_label()
        
        return self.asm_instructions


    def increment_label(self):
        self.label_cnt += 1




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accepts file and removes whitespace/comments")
    parser.add_argument('file_path',type=str, metavar='file_path', help="file_path")  
    
    args = parser.parse_args()

    file_in = args.file_path
    file_out = Reader(file_in)
    instrutions = file_out.clean_instructions()
    translator = Translator(instrutions)
    asm_instructions = translator.translate()
    file_out.output(asm_instructions)






