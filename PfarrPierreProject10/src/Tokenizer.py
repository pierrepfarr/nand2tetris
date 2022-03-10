class Tokenizer:
    
    symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','|','=','~']
    keywords = ["class","constructor","function","method","field",
                "static","var","int","char","boolean","void","true","false",
                "null","this","let","do","if","else","while","return"]
    xml = {">":"&gt;",
           "<":"&lt;",
           "&":"&amp;",
           "\"":"&quot;"}

    def __init__(self,instr) -> None:
        self.instructions = instr
        self.end = len(instr)-1
        self.idx = 0
        self.tokens = []
        self.current = None
        self.current_type = None
        

    def get_all_tokens(self):
        more_tokens = self.tokens_left()
        while more_tokens:
            self.get_token()
            more_tokens = self.tokens_left()

    def get_token(self):
        char = self.get_char()
        next_char = self.get_next_char()
        new_token = ""

        if char.isspace():
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()

        elif char.isalpha() or char.isnumeric():
            while next_char.isalpha() or next_char.isnumeric() or next_char == "_":
                new_token += char
                self.idx += 1
                char = self.get_char()
                next_char = self.get_next_char()
            new_token += char
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()
    
        elif char == "\"":
            new_token += char
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()
            while char != "\"":
                new_token += char
                self.idx += 1
                char = self.get_char()
                next_char = self.get_next_char()
            
            new_token += char
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()

        elif char in self.symbols:
            new_token = char
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()

        else:
            new_token = self.xml[char]
            self.idx += 1
            char = self.get_char()
            next_char = self.get_next_char()

        if new_token != "":
            self.current = new_token
            self.current_type = self.get_type()
            if self.current_type == "stringConstant":
                self.tokens.append((self.current[1:-1],self.current_type))
            else:
                self.tokens.append((self.current,self.current_type))
        

    def get_type(self):
        if self.current in self.keywords:
            return "keyword"
        if self.current in self.symbols or self.current in self.xml.values():
            return "symbol"
        if self.current.startswith("\""):
            return "stringConstant"
        if self.current.isnumeric():
            return "integerConstant"
        if self.current.isalnum():
            return "identifier"
        else:
            return "not_found"

    def get_char(self):
        if self.idx <= self.end:
            return self.instructions[self.idx]
        else:
            return None
    
    def get_next_char(self):
        if self.idx < self.end:
            return self.instructions[self.idx+1]
        else:
            return None

    def tokens_left(self):
        return self.idx <= self.end
    

    