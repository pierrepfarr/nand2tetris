class Memory_Access:

    """registers that point at starting segment"""    
    memory_segments = { "SP": 0,
                        "local":1,
                        "argument":2,
                        "this":3,
                        "that":4
                        }
    """registers that are fixed and don't point away""" 
    fixed_memory_segments = {"pointer":3,
                             "temp":5,
                             "static":16}

    def __init__(self,instruction,fname):
        self.instruction = instruction
        self.fname = fname
        self.command, self.segment, self.index = self.__break(instruction)
        self.asm_instructions=[]

    def __break(self,instruction):
        """ break apart the instruction"""
        parts = instruction.split(" ")
        command = parts[0]
        segment = parts[1]
        index = parts[2]
        return command, segment, index

    
    def translate(self):
        """check for for pop or push and call the logic"""
        
        if self.command == "pop":
            if self.segment == "static":
                pop = self.get_from_stack() # get stack val
                load = f"@{self.fname}.{self.index}\n" #load static location
                set = "M=D\n"

                self.asm_instructions.append(pop)
                self.asm_instructions.append(load)
                self.asm_instructions.append(set)

            else:
                load = self.load_addr() # load the segment addr
                store = self.store_addr(index=0) # store the addr
                pop = self.get_from_stack() # get stack val
                store_2 = self.store_addr(index=1) # store the stack val
                set = self.set_addr_to_pop() # set the addr to val

                self.asm_instructions.append(load)
                self.asm_instructions.append(store)
                self.asm_instructions.append(pop)
                self.asm_instructions.append(store_2)
                self.asm_instructions.append(set)

        else:
            if self.segment == "static":
                load = f"@{self.fname}.{self.index}\n"
                get_value = "D=M\n"  #get static value
                put = self.put_on_stack() 
                move = self.increment_sp()

                self.asm_instructions.append(load)
                self.asm_instructions.append(get_value)
                self.asm_instructions.append(put)
                self.asm_instructions.append(move)
                
            else:
                load = self.load_addr() # load addr
                if self.segment != "constant":
                    value = self.get_value_at_addr() # if not constant get value at addr
                else:
                    value = False
                put = self.put_on_stack() # put on stack
                move = self.increment_sp() # move pointer
                 
                self.asm_instructions.append(load)
                if value: self.asm_instructions.append(value)
                self.asm_instructions.append(put)
                self.asm_instructions.append(move)

    
    def load_addr(self):
        """loads the address of the register we want"""
        if self.segment in self.memory_segments:
            addr = self.memory_segments.get(self.segment)
            instr = [f"@{addr}\n",
                    "D=M\n",
                    f"@{self.index}\n",
                    "D=D+A\n"]
            return ''.join(instr)
        
        elif self.segment in self.fixed_memory_segments:
            addr = self.fixed_memory_segments.get(self.segment) + int(self.index)
            instr = [f"@{addr}\n",
                    "D=A\n",]
            return ''.join(instr)
        
        else:
            instr = [f"@{self.index}\n",
                    "D=A\n"]
            return ''.join(instr)

    def store_addr(self,index):
        """Store D in one of our General Purpose Registers """
       
        register = 13+int(index)
        instr = [f"@R{register}\n",
                "M=D\n"]
        return ''.join(instr)
 
    def get_value_at_addr(self):
        """ gets the value of a register we are at"""
        instr = ["A=D\n",
                 "D=M\n"]
        return ''.join(instr)
    
    def get_from_stack(self):
        """Load Pointer, Decrement, Set SP Memory and Address,
           Store Address Memory in D"""
        
        instr = ["@SP\n",
                 "AM=M-1\n",
                 "D=M\n"]
        return ''.join(instr)
    
    
    def set_addr_to_pop(self):
        """put stored value in the stored address"""
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
                 "M=M+1\n"]
        return ''.join(instr)

    