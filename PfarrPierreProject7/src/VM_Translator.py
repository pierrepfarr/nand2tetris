class Translator:

    def __init__(self,instructions):
        self.vm_instructions = instructions
        self.asm_instructions = None



class Memory_Instruction:
    local = 1
    arg = 2
    this = 3
    that = 4


    def __init__(self,instruction):
        self.command, self.segment, self.index = self.__break(instruction)
        self.asm_instruction=[]

    def __break(self,instruction):
        parts = instruction.split(" ")
        command = parts[0]
        segment = parts[1]
        index = parts[2]
        return command, segment, index

    
    
    
    def put_on_stack(self):
        instr = ["@SP\n",
                 "A=M\n",
                 "M=D\n"]
        return ''.join(instr)
    
    def increment_sp(self):
        instr = ["@SP\n",
                 "M=M+1"]
        return ''.join(instr)



