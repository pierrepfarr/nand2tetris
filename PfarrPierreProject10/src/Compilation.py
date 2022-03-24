class Compilation:
    classVarDec = ["static","field"]
    subroutineDec = ["constructor","function","method"]
    operators = ["+","-","*","/","&amp;","|","&lt;","&gt;","="]
    unary = ["~","-"]


    def __init__(self,tokens) -> None:
        self.tokens = tokens
        self.idx = 0
        self.end = len(tokens)-1
        self.current = tokens[0][0]
        self.current_type = tokens[0][1]
        self.output = []

    def compile_class(self):
        
        if self.idx <= self.end:
            self.output.append(self.generate_tag("class")+"\n")
            
            self.next()
            self.next()
            self.next()

        while self.idx < self.end: # while not at the end of the token list
            if self.current in self.classVarDec: #if field of static
                self.compile_classVarDec() 
            elif self.current in self.subroutineDec: #if constructor function or method
                self.compile_subroutine()
        
        self.next()
        
        self.output.append(self.generate_tag("/class")+"\n")
            


    def compile_classVarDec(self):
        self.output.append(self.generate_tag("classVarDec")+"\n")
        
        self.next() #static/field    
        self.next() #type
        self.next() #identifier

        while self.current == ",": # if other identifiers then output , and id
            self.next()
            self.next()

        
        self.next() #;

        self.output.append(self.generate_tag("/classVarDec")+"\n")

    def compile_subroutine(self):
        self.output.append(self.generate_tag("subroutineDec")+"\n")
        
        self.next() #function
        self.next() #void
        self.next() #identifier
        self.next() #{


        self.compile_parameters() #parameters empty or many

        self.next() #;
        
        self.compile_subroutineBody()

        self.output.append(self.generate_tag("/subroutineDec")+"\n")



    def compile_parameters(self):
        self.output.append(self.generate_tag("parameterList")+"\n")

        while self.current_type == "keyword" or self.current_type == "identifier":
            self.next()
            self.next()
            
            if self.current == ",":
                self.next()
                
        
        self.output.append(self.generate_tag("/parameterList")+"\n")
            

    
    def compile_subroutineBody(self):
        self.output.append(self.generate_tag("subroutineBody")+"\n")
        self.next()
        

        while self.current == "var":
            self.compile_varDec()
        
        self.compile_statements() # compile all keywords matching statements
        self.next()
        

        self.output.append(self.generate_tag("/subroutineBody")+"\n")



    def compile_varDec(self):
        self.output.append(self.generate_tag("varDec")+"\n")
        
        self.next() #similar to classvardec
        self.next()
        self.next()
        

        while self.current == ",":
            self.next()
            self.next()
            
        self.next()
        self.output.append(self.generate_tag("/varDec")+"\n")

    def compile_statements(self):
        statements = {"let":self.compile_let,
                      "if":self.compile_if,
                      "do":self.compile_do,                      
                      "while":self.compile_while,
                      "return":self.compile_return}

        self.output.append(self.generate_tag("statements")+"\n")

        while self.current_type == "keyword":
            if self.current in statements:
                statements[self.current]()
                 
        self.output.append(self.generate_tag("/statements")+"\n")

    def compile_let(self):
        self.output.append(self.generate_tag("letStatement")+"\n")

        self.next()
        self.next()
        

        if self.current == "[":
            self.next()#identifier/index
            self.compile_expression()
            self.next()#close the bracket
            

        self.next()
        
        self.compile_expression()

        self.next()
        

        self.output.append(self.generate_tag("/letStatement")+"\n")
    

    def compile_if(self):
        self.output.append(self.generate_tag("ifStatement")+"\n")    
        self.next()
        self.next()
        

        self.compile_expression()
        
        self.next()
        self.next()
        

        self.compile_statements()

        self.next()
        
        
        if self.current == "else":
            self.next()
            self.next()
            
            self.compile_statements()
            
            self.next()
            
        
        self.output.append(self.generate_tag("/ifStatement")+"\n")


    def compile_while(self):
        self.output.append(self.generate_tag("whileStatement")+"\n")
        
        self.next()
        self.next()
        
        self.compile_expression()

        self.next()
        self.next()
        

        self.compile_statements()
        self.next()
        
    
        self.output.append(self.generate_tag("/whileStatement")+"\n")

    def compile_do(self):
        self.output.append(self.generate_tag("doStatement")+"\n")

        self.next()
        self.next()
        

        if self.current == ".": #method call
            self.next()
            self.next()
            
    
        self.next()
    
        self.compile_expressions()

        self.next()
        self.next()
        

        self.output.append(self.generate_tag("/doStatement")+"\n")

    def compile_return(self):
        self.output.append(self.generate_tag("returnStatement")+"\n")
        self.next()
        

        if self.current != ";":
            self.compile_expression()
        
        self.next()
        
        self.output.append(self.generate_tag("/returnStatement")+"\n")

    def compile_expression(self):
        self.output.append(self.generate_tag("expression")+"\n")
        self.compile_term()

        if self.current in self.operators:
            self.next()
            self.compile_term()
        self.output.append(self.generate_tag("/expression")+"\n")


    def compile_expressions(self):
        self.output.append(self.generate_tag("expressionList")+"\n")
        
        if self.current == "(" or self.current != ")":
            self.compile_expression()
            while self.current == ",":
                self.next()
                self.compile_expression()
        
        self.output.append(self.generate_tag("/expressionList")+"\n")
        

    def compile_term(self):
        self.output.append(self.generate_tag("term")+"\n")
        
        if self.current_type == "identifier":
            self.next()

            if self.current == "(":
                self.next()
                self.compile_expressions()
                self.next()
                   
            elif self.current == ".":
                self.next()
                self.next()
                self.next()
                
                self.compile_expressions()
                self.next()
                
            elif self.current == "[":
                self.next()
                self.compile_expression()
                self.next()
                
        elif self.current in self.unary:
            self.next()
            self.compile_term()
        
        elif self.current == "(":
            self.next()
            self.compile_expression()
            self.next()
            
        else:
            self.next()
            
        self.output.append(self.generate_tag("/term")+"\n")

    def generate_tag(self,tag):
        return f"<{tag}>"
    
    def generate_current_tag(self):
        tag = [] 
        curr_token = self.current
        curr_type = self.current_type
        tag.append(self.generate_tag(curr_type))
        tag.append(curr_token)
        tag.append(self.generate_tag("/"+curr_type))
        tag.append("\n")
        return ''.join(tag)

    def advance(self):
        if self.idx < self.end:
            self.idx += 1
            self.current = self.tokens[self.idx][0]
            self.current_type = self.tokens[self.idx][1]
        else:
            self.idx += 1

    def next(self):
        self.output.append(self.generate_current_tag())
        self.advance()
        
