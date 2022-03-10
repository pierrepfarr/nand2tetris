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
            
            self.output.append(self.generate_current_tag())
            self.advance()
            self.output.append(self.generate_current_tag())
            self.advance()
            self.output.append(self.generate_current_tag())
            self.advance()


        while self.idx < self.end: # while not at the end of the token list
            if self.current in self.classVarDec: #if field of static
                self.compile_classVarDec() 
            elif self.current in self.subroutineDec: #if constructor function or method
                self.compile_subroutine()
        
        self.output.append(self.generate_current_tag())
        self.advance()
        
        self.output.append(self.generate_tag("/class")+"\n")
            


    def compile_classVarDec(self):
        self.output.append(self.generate_tag("classVarDec")+"\n")
        
        self.output.append(self.generate_current_tag()) #static/field
        self.advance()
        self.output.append(self.generate_current_tag()) #type
        self.advance()
        self.output.append(self.generate_current_tag()) #identifier
        self.advance()

        while self.current == ",": # if other identifiers then output , and id
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.output.append(self.generate_current_tag()) 
            self.advance()
        
        self.output.append(self.generate_current_tag()) #;
        self.advance()

        self.output.append(self.generate_tag("/classVarDec")+"\n")

    def compile_subroutine(self):
        self.output.append(self.generate_tag("subroutineDec")+"\n")
        
        self.output.append(self.generate_current_tag()) #function
        self.advance() 
        self.output.append(self.generate_current_tag()) #void
        self.advance()
        self.output.append(self.generate_current_tag()) #identifier
        self.advance()
        self.output.append(self.generate_current_tag()) #{
        self.advance()

        self.compile_parameters() #parameters empty or many

        self.output.append(self.generate_current_tag()) #;
        self.advance() 
        
        self.compile_subroutineBody()

        self.output.append(self.generate_tag("/subroutineDec")+"\n")



    def compile_parameters(self):
        self.output.append(self.generate_tag("parameterList")+"\n")

        while self.current_type == "keyword" or self.current_type == "identifier":
            self.output.append(self.generate_current_tag()) 
            self.advance()
        
            self.output.append(self.generate_current_tag()) 
            self.advance()

            if self.current == ",":
                self.output.append(self.generate_current_tag()) 
                self.advance()
        
        self.output.append(self.generate_tag("/parameterList")+"\n")
            

    
    def compile_subroutineBody(self):
        self.output.append(self.generate_tag("subroutineBody")+"\n")
        
        self.output.append(self.generate_current_tag()) 
        self.advance()

        while self.current == "var":
            self.compile_varDec()
        
        self.compile_statements() # compile all keywords matching statements

        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.output.append(self.generate_tag("/subroutineBody")+"\n")



    def compile_varDec(self):
        self.output.append(self.generate_tag("varDec")+"\n")
        
        self.output.append(self.generate_current_tag())  #similar to classvardec
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        while self.current == ",":
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.output.append(self.generate_current_tag()) 
            self.advance()
        
        self.output.append(self.generate_current_tag()) 
        self.advance()

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

        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        if self.current == "[":
            self.output.append(self.generate_current_tag()) #identifier/index
            self.advance()
            self.compile_expression()
            self.output.append(self.generate_current_tag()) #close the bracket
            self.advance()

        self.output.append(self.generate_current_tag()) 
        self.advance()
        
        self.compile_expression()

        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.output.append(self.generate_tag("/letStatement")+"\n")
    


    def compile_if(self):
        self.output.append(self.generate_tag("ifStatement")+"\n")
        
        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.compile_expression()
        
        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.compile_statements()

        self.output.append(self.generate_current_tag()) 
        self.advance()
        
        if self.current == "else":
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.output.append(self.generate_current_tag()) 
            self.advance()

            self.compile_statements()
            
            self.output.append(self.generate_current_tag()) 
            self.advance()
        
        self.output.append(self.generate_tag("/ifStatement")+"\n")


    def compile_while(self):
        self.output.append(self.generate_tag("whileStatement")+"\n")
        
        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.compile_expression()

        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.compile_statements()

        self.output.append(self.generate_current_tag()) 
        self.advance()
    
        self.output.append(self.generate_tag("/whileStatement")+"\n")

    def compile_do(self):
        self.output.append(self.generate_tag("doStatement")+"\n")

        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        if self.current == ".": #method call
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.output.append(self.generate_current_tag()) 
            self.advance()
    
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.compile_expressions()

        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_current_tag()) 
        self.advance()

        self.output.append(self.generate_tag("/doStatement")+"\n")

    def compile_return(self):
        self.output.append(self.generate_tag("returnStatement")+"\n")
        self.output.append(self.generate_current_tag()) 
        self.advance()

        if self.current != ";":
            self.compile_expression()
        
        self.output.append(self.generate_current_tag()) 
        self.advance()
        self.output.append(self.generate_tag("/returnStatement")+"\n")

    def compile_expression(self):
        self.output.append(self.generate_tag("expression")+"\n")
        self.compile_term()

        if self.current in self.operators:
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.compile_term()
        self.output.append(self.generate_tag("/expression")+"\n")



    def compile_expressions(self):
        self.output.append(self.generate_tag("expressionList")+"\n")
        
        if self.current == "(" or self.current != ")":
            self.compile_expression()
            while self.current == ",":
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.compile_expression()
        
        self.output.append(self.generate_tag("/expressionList")+"\n")
        

    def compile_term(self):
        self.output.append(self.generate_tag("term")+"\n")
        
        if self.current_type == "identifier":
            self.output.append(self.generate_current_tag()) 
            self.advance()

            if self.current == "(":
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.compile_expressions()
                self.output.append(self.generate_current_tag()) 
                self.advance()   
            elif self.current == ".":
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.compile_expressions()
                self.output.append(self.generate_current_tag()) 
                self.advance()
            elif self.current == "[":
                self.output.append(self.generate_current_tag()) 
                self.advance()
                self.compile_expression()
                self.output.append(self.generate_current_tag()) 
                self.advance()

        elif self.current in self.unary:
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.compile_term()
        elif self.current == "(":
            self.output.append(self.generate_current_tag()) 
            self.advance()
            self.compile_expression()
            self.output.append(self.generate_current_tag()) 
            self.advance()
        else:
            self.output.append(self.generate_current_tag()) 
            self.advance()

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
