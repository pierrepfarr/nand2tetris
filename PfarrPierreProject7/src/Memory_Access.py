class Memory_Access:

    memory_segments = { "SP": 0,
                        "local":1,
                        "argument":2,
                        "this":3,
                        "that":4,
                        "pointer":3,
                        "temp":5,
                        "static":16
                        }

    def __init__(self,instruction):
        self.command, self.segment, self.index = self.__break(instruction)
        self.asm_instructions=[]

    def __break(self,instruction):
        parts = instruction.split(" ")
        command = parts[0]
        segment = parts[1]
        index = parts[2]
        return command, segment, index

    
    def translate(self):
        if self.command == "pop":
            load = self.load()
            store = self.store_addr(index=0)
            top = self. get_from_stack()
            store_2 = self.store_addr(index=1)
            set = self.set_addr_to_pop()

            self.asm_instructions.append(load)
            self.asm_instructions.append(store)
            self.asm_instructions.append(top)
            self.asm_instructions.append(store_2)
            self.asm_instructions.append(set)

        else:
            load = self.load()
            put = self.put_on_stack()
            move = self.increment_sp()
            
            self.asm_instructions.append(load)
            self.asm_instructions.append(put)
            self.asm_instructions.append(move)

    
    def load(self):
        if self.segment in self.memory_segments:
            addr = self.memory_segments.get(self.segment) + self.index
            instr = [f"@{addr}\n",
                    "D=A\n"]
            return ''.join(instr)
        else:
            instr = [f"@{self.index}\n",
                    "D=A\n"]
            return ''.join(instr)

    def store_addr(self,index):
        """Store D in one of our General Purpose Registers """
       
        register = 13+index
        instr = [f"@R{register}\n",
                "M=D\n"]
        return ''.join(instr)
 
 
    def get_from_stack(self):
        """Load Pointer, Decrement, Set SP Memory and Address,
           Store Address Memory in D"""
        
        instr = ["@SP\n",
                 "AM=M-1\n",
                 "D=M\n"]
        return ''.join(instr)
    
    
    def set_addr_to_pop(self):
        instr = ["@R14\n",
                 "D=M\n",
                 "@R13\n",
                 "A=M\n",
                 "M=D\n"]
        return ''.join(instr)
    
    def put_on_stack(self):
        instr = ["@SP\n",
                 "A=M\n",
                 "M=D\n"]
        return ''.join(instr)
    
    def increment_sp(self):
        instr = ["@SP\n",
                 "M=M+1"]
        return ''.join(instr)