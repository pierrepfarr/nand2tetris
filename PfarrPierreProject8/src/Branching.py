class Branching:

    def __init__(self,instruction):
        self.instruction = instruction
        self.command, self.label = self.__break(instruction)
        self.asm_instructions=[]


    def __break(self,instruction):
        """ break apart the instruction"""
        parts = instruction.split(" ")
        command = parts[0]
        label = parts[1]
        return command, label

    def translate(self):
        if self.command == "label":
            instr = self.assign_label()
            self.asm_instructions.append(instr)
        elif self.command == "goto":
            instr = self.goto()
            self.asm_instructions.append(instr)
        else:
            instr = self.if_goto()
            self.asm_instructions(instr)
        
    def assign_label(self):
        """assign a label an address"""
        return f"@{self.label}\n"

    def goto(self):
        """unconditional jmp to label"""
        instr = [f"@{self.label}\n",
                 "0;JMP\n"]
        return ''.join(instr)

    def if_goto(self):
        """pop the truth value and if not false then jmp to label"""
        pop = self.get_from_stack()
        instr = [f"@{self.label}\n",
                 "D;JNE\n"]
        instr = pop.extend(instr)
        return ''.join(instr)

    def get_from_stack(self):
        """Load Pointer, Decrement, Set SP Memory and Address,
           Store Address Memory in D"""
        
        instr = ["@SP\n",
                 "AM=M-1\n",
                 "D=M\n"]
        return ''.join(instr)