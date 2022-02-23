class Functions:

    def __init__(self,instruction):
        self.instruction = instruction
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

    def return_call(self):
        pass

    def func_def(self):
        pass

    def func_call(self):
        pass