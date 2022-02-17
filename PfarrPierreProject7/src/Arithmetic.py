class Stack_Arithmetic:
    asm_logic = { "eq":"JEQ\n",
                  "lt":"JLT\n",
                  "gt":"JGT\n",
                  "add":"M=M+D\n",
                  "sub":"M=M-D\n",
                  "and":"M=M&D\n",
                  "or":"M=M|D\n",
                  "not":"M=!M\n",
                  "neg":"M=-M\n" }

    
    def __init__(self,instruction,label_count):
        self.instruction = instruction
        self.label_cnt = label_count
        self.asm_instructions=[]

    def translate(self):
        pass

    def jump(self):
        logic = self.asm_logic[self.instruction]
        
        pop_1 = self.get_from_stack()
        into_D = "D=M\n"
        pop_2 = self.get_from_stack()
        diff_D = "D=M-D\n"    #diff is in d
        
        temp_truth = "M=-1\n" #set stack to true
        load_label = f"@{self.instruction}_{self.label_cnt}\n"
        jump = f"D;{logic}\n"

        at_sp = "@SP\n"
        move = "A=M\n"
        set_false = "M=0\n"

        set_label = f"({self.instruction}_{self.label_cnt})\n"

        self.asm_instructions.append(pop_1)
        self.asm_instructions.append(into_D)
        self.asm_instructions.append(pop_2)
        self.asm_instructions.append(diff_D)
        self.asm_instructions.append(temp_truth)
        self.asm_instructions.append(load_label)
        self.asm_instructions.append(jump)
        self.asm_instructions.append(at_sp)
        self.asm_instructions.append(move)
        self.asm_instructions.append(set_false)
        self.asm_instructions.append(set_label)


    def binary(self):
        pop_1 = self.get_from_stack()
        into_D = "D=M\n"
        pop_2 = self.get_from_stack()
        logic = self.asm_logic[self.instruction]
        move = self.increment_sp()

        self.asm_instructions.append(pop_1)
        self.asm_instructions.append(into_D)
        self.asm_instructions.append(pop_2)
        self.asm_instructions.append(logic)
        self.asm_instructions.append(move)


    def unary(self):
        pop = self.get_from_stack()
        logic = self.asm_logic[self.instruction]
        move = self.increment_sp()

        self.asm_instructions.append(pop)
        self.asm_instructions.append(logic)
        self.asm_instructions.append(move)

    def get_from_stack(self):
        """Load Pointer, Decrement, Set SP Memory and Address"""

        instr = ["@SP\n",
                 "AM=M-1\n"]
        return ''.join(instr)

    def increment_sp(self):
        instr = ["@SP\n",
                 "M=M+1\n"]
        return ''.join(instr)

    