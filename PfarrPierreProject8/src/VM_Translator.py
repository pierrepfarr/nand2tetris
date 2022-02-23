from Branching import Branching
from VM_Reader import Reader
from Arithmetic import Stack_Arithmetic
from Memory_Access import Memory_Access

import argparse
import glob
import os

class Translator:

    def __init__(self,instructions,label_cnt=0):
        self.vm_instructions = instructions
        self.asm_instructions = []
        self.label_cnt = label_cnt

    def translate(self):
        """check for vm instruction and translate storing to asm_instr list"""
        for instruction in self.vm_instructions:
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
    parser = argparse.ArgumentParser(description="Accepts folder path")
    parser.add_argument('folder_path',type=str, metavar='folder_path', help="folder_path")  
    
    args = parser.parse_args()

    folder = args.folder_path
    folder_dir = os.path.abspath(folder)

    vm_files = glob.glob(folder_dir+"/*.vm")
    
    label_cnt = 0
    asm_instructions = []
    
    for file_in in vm_files:
        file_out = Reader(file_in)
        vm_instructions = file_out.clean_instructions()
        translator = Translator(vm_instructions,label_cnt)
        file_asm_instructions = translator.translate()
        label_cnt = translator.label_cnt
        asm_instructions.extend(file_asm_instructions)
    
    file_out.output(asm_instructions)





