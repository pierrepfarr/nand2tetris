from multiprocessing.spawn import old_main_modules


class Functions:

    def __init__(self,instruction,label_count):
        self.instruction = instruction
        self.label_cnt = label_count
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
        if self.command == "function":
            self.func_def()
        elif self.command == "call":
            self.func_call()
        else:
            self.return_call()

    def func_def(self):
        label = f"({self.function})\n"
        int_vars = int(self.nvars)
        push_vars = self.push_zeros(int_vars)

        self.asm_instructions.append(label)
        self.asm_instructions.append(push_vars)

    def push_zeros(self,times):
        instr = [] 
        for i in range(times):
            push = ["@SP\n",
                    "A=M\n",
                    "M=0\n",]
            push = ''.join(push)
            instr.append(push)
            instr.append(self.increment_sp())
        return ''.join(instr)
  
    def func_call(self):
        ret_addr = f"@{self.function}.{self.label_cnt}\n"
        load_adrr = "D=A\n"
        put_adrr = self.put_on_stack()
        incr_sp_1 = self.increment_sp()
        push_lcl = self.push_mem_segment("LCL")
        push_arg = self.push_mem_segment("ARG")
        push_this = self.push_mem_segment("THIS")
        push_that = self.push_mem_segment("THAT")
        set_arg = self.call_set_arg()
        set_lcl= self.set_local()
        jmp_func = self.jmp_to_func()
        ret_label = f"({self.function}.{self.label_cnt})\n"

        self.asm_instructions.append(ret_addr)
        self.asm_instructions.append(load_adrr)
        self.asm_instructions.append(put_adrr)
        self.asm_instructions.append(incr_sp_1)
        self.asm_instructions.append(push_lcl)
        self.asm_instructions.append(push_arg)
        self.asm_instructions.append(push_this)
        self.asm_instructions.append(push_that)
        self.asm_instructions.append(set_arg)
        self.asm_instructions.append(set_lcl)
        self.asm_instructions.append(jmp_func)
        self.asm_instructions.append(ret_label)



    def push_mem_segment(self,segment):
        instr = [f"@{segment}\n",
                 "D=M\n",
                 "@SP\n",
                 "A=M\n",
                 "M=D\n",
                 "@SP\n",
                 "M=M+1\n"]
        return ''.join(instr)

    def call_set_arg(self):
        first_arg = 5 + int(self.nvars)
        instr = ["@SP\n",
                 "D=M\n",
                 f"@{first_arg}\n",
                 "D=D-A\n",
                 "@ARG\n",
                 "M=D\n"]
        return ''.join(instr)

    def set_local(self):
        instr = ["@SP\n",
                 "D=M\n",
                 "@LCL\n",
                 "M=D\n"]
        return ''.join(instr)
    
    
    def jmp_to_func(self):
        instr = [f"@{self.fname}_{self.function}\n",
                 "0;JMP\n"]
        return ''.join(instr)


    
    
    def return_call(self):
        get_local = self.get_local()
        frame = "@FRAME\n"
        set_frame = "M=D\n"
        get_return_addr = self.get_registers_before_frame(5)
        load_temp_ret = "@RET\n"
        set_temp_ret = "M=D\n"
        pop = self.get_from_stack()
        goto_arg = self.goto_arg()
        return_res = "M=D\n"
        move_sp = self.set_sp_after_arg()
        get_that = self.get_registers_before_frame(1)
        set_that = self.set_segment("THAT")
        get_this = self.get_registers_before_frame(2)
        set_this = self.set_segment("THIS")
        get_arg = self.get_registers_before_frame(3)
        set_arg = self.set_segment("ARG")
        get_lcl = self.get_registers_before_frame(4)
        set_lcl = self.set_segment("LCL")
        load_temp_ret2 = "@RET\n"
        load_addr = "A=M\n"
        jmp = "0;JMP\n"


        self.asm_instructions.append(get_local)
        self.asm_instructions.append(frame)
        self.asm_instructions.append(set_frame)
        self.asm_instructions.append(get_return_addr)
        self.asm_instructions.append(load_temp_ret)
        self.asm_instructions.append(set_temp_ret)
        self.asm_instructions.append(pop)
        self.asm_instructions.append(goto_arg)
        self.asm_instructions.append(return_res)
        self.asm_instructions.append(move_sp)
        self.asm_instructions.append(get_that)
        self.asm_instructions.append(set_that)
        self.asm_instructions.append(get_this)
        self.asm_instructions.append(set_this)
        self.asm_instructions.append(get_arg)
        self.asm_instructions.append(set_arg)
        self.asm_instructions.append(get_lcl)
        self.asm_instructions.append(set_lcl)
        self.asm_instructions.append(load_temp_ret2)
        self.asm_instructions.append(load_addr)
        self.asm_instructions.append(jmp)


    def get_local(self):
        instr = ["@LCL\n",
                 "D=M\n"]
        return ''.join(instr)


    def get_registers_before_frame(self,num):
        instr = [f"@{num}\n",
                 "D=A\n",
                 "@FRAME\n",
                 "A=M-D\n",
                 "D=M\n"]
        return ''.join(instr)

    def set_segment(self,segment):
        instr = [f"@{segment}\n",
                 "M=D\n"]
        return ''.join(instr)

    def goto_arg(self):
        instr = ["@ARG\n",
                 "A=M\n"]
        return ''.join(instr)       
    
    def set_sp_after_arg(self):
        instr = ["@ARG\n",
                 "D=M+1\n",
                 "@SP\n",
                 "M=D\n"]
        return ''.join(instr)    


    def put_on_stack(self):
        instr = ["@SP\n",
                 "A=M\n",
                 "M=D\n"]
        return ''.join(instr)

    def get_from_stack(self):
        """Load Pointer, Decrement, Set SP Memory and Address,
           Store Address Memory in D"""
        
        instr = ["@SP\n",
                 "AM=M-1\n",
                 "D=M\n"]
        return ''.join(instr)

    def increment_sp(self):
        instr = ["@SP\n",
                 "M=M+1\n"]
        return ''.join(instr)