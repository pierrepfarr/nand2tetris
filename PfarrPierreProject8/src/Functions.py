class Functions:

    def __init__(self,instruction,fname):
        self.instruction = instruction
        self.fname = fname
        self.command, self.function, self.nvars = self.__break(instruction)
        self.asm_instructions=[]   

    def __break(self,instruction):
        """ break apart the instruction"""
        parts = instruction.split(" ")
        if parts[0] == "return":
            return parts[0],None,None
        else:
            command = parts[0]
            function = parts[1]
            nvars = parts[2]
            return command, function, nvars


    def translate(self):
        pass

    def func_def(self):
        label = f"({self.fname}_{self.function})\n"
        int_vars = int(self.nvars)
        push_vars = self.push_zeros(int_vars)

        self.asm_instructions.append(label)
        self.asm_instructions.append(push_vars)

    def func_call(self):
        pass

    
    def return_call(self):
        pass

    def push_zeros(self,times):
        instr = [] 
        for i in range(times):
            push = ["@SP\n",
                    "A=M\n",
                    "M=0\n",]
            instr.extend(push)
            instr.extend(self.increment_sp())
        return ''.join(instr)

    
    def increment_sp(self):
        instr = ["@SP\n",
                    "M=M+1\n"]
        return ''.join(instr)