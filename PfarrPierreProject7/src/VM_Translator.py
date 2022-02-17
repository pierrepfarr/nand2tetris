
from numpy import diff


class Translator:

    def __init__(self,instructions):
        self.vm_instructions = instructions
        self.asm_instructions = None



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
            pop = self. get_from_stack()
            store_2 = self.store_addr(index=1)
            set = self.set_addr_to_pop()

            self.asm_instructions.append(load)
            self.asm_instructions.append(store)
            self.asm_instructions.append(pop)
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
                 "M=M+1\n"]
        return ''.join(instr)



