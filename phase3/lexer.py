import sys

# tokens

# keywords
KEYWORDS = {
    'if':       'IF',          
    'else':     'ELSE',        
    'while':    'WHILE',       
    'int':      'INT',         
    'float':    'FLOAT',       
    'void':     'VOID',        
    'call':     'CALL',        
    'print':    'PRINT',       
    'read':     'READ',        
    'function': 'FUNCTION',    
    'main':     'MAIN',        
    'return':   'RETURN'       
}

class Lexer:
    def __init__(self,filename):
        try:
            with open(filename, 'r') as f:
                self.text = f.read()
        except IOError:
            print("error opening the file", filename)
            sys.exit(1)
        self.pos = 0
        # if there is text lex is filled with the current ch 
        # else theres nothing to process
        self.current_char = self.text[self.pos] if self.text else None

    def error(self, message):
        print("Lexer error:", message)
        sys.exit(1)

    # lexer advance
    def advance(self):
        # advance the pointer and set the current ch 
        self.pos +=1
        # advancing within text
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else: 
            self.current_char = None

    # lexer peek
    def peek(self):
        # look ahead the next ch   
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None
    
    # whitespace
    def skip_whitespace(self):
        # current ch exist and is a space
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    # identifiers
    def identifier(self):
        # return an identifier or keyword
        result = ''
        # keywords and _
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        token_type = KEYWORDS.get(result, 'ID')
        return {'token': token_type, 'tokenText': result}
    
    # integer and floating constant
    def number(self):
        result = ''
        # collect the integer part
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # if we see a dot add it and move the pointer and collect the digits after the dot
        if self.current_char == '.':
            result += '.'
            self.advance()
            # Collect zero or more digits after the dot
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token_type = 'FCONST'
        else:
            token_type = 'ICONST'

        return {'token': token_type, 'tokenText': result}
    
    # skip comment = no token return
    def skip_comment(self):
        # scan past the text and then start over scanning for another token
        # skipping /* first
        self.advance() 
        self.advance()

        # scanning past the string within comment
        while self.current_char is not None:
            # end of the comment */
            if self.current_char == '*' and self.peek() == '/':
                self.advance() 
                self.advance()
                return
            
            # characters within the comment
            self.advance()
    
    def getNextToken(self):
        # scan the input and return the next token
        while self.current_char is not None:

            # recognize explicit end-of-input marker $$
            if self.current_char == '$' and self.peek() == '$':
                self.advance()
                self.advance()
                return {'token': 'DD', 'tokenText': '$$'}

            # skip white space
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # handle comment
            if self.current_char == '/':
                if self.peek() == '*':
                    self.skip_comment()
                    continue
                else: # division /
                    self.advance()
                    return {'token': 'DIV', 'tokenText':'/'}

            # punctuation
            if self.current_char == ';':
                self.advance()
                return {'token': 'SEMICOLON', 'tokenText': ';'}
            if self.current_char == '(':
                self.advance()
                return {'token': 'LPAREN', 'tokenText': '('}
            if self.current_char == ')':
                self.advance()
                return {'token': 'RPAREN', 'tokenText': ')'}
            if self.current_char == ',':
                self.advance()
                return {'token': 'COMMA', 'tokenText': ','}
            if self.current_char == '{':
                self.advance()
                return {'token': 'LBRACE', 'tokenText': '{'}
            if self.current_char == '}':
                self.advance()
                return {'token': 'RBRACE', 'tokenText': '}'}
            if self.current_char == '[':
                self.advance()
                return {'token': 'LBRACKET', 'tokenText': '['}
            if self.current_char == ']':
                self.advance()
                return {'token': 'RBRACKET', 'tokenText': ']'}
            
            # operators
            # = 
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    # ==
                    return {'token': 'EQUAL', 'tokenText': '=='}
                else:
                    self.advance()
                    return {'token': 'ASSIGN', 'tokenText': '='}
            
            # <, <=
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return {'token': 'LE', 'tokenText': '<='}
                else:
                    self.advance()
                    return {'token': 'LT', 'tokenText': '<'}
            # >, >=
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return {'token': 'GE', 'tokenText': '>='}
                else:
                    self.advance()
                    return {'token': 'GT', 'tokenText': '>'}
            # !, != 
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return {'token': 'NOTEQUAL', 'tokenText': '!='}
                else:
                    self.advance()
                    return {'token': 'NOT', 'tokenText': '!'}
            # +, -, *, /
            if self.current_char == '+':
                self.advance()
                return {'token': 'PLUS', 'tokenText': '+'}
            if self.current_char == '-':
                self.advance()
                return {'token': 'MINUS', 'tokenText': '-'}
            if self.current_char == '*':
                self.advance()
                return {'token': 'MULT', 'tokenText': '*'}
            # &&
            if self.current_char == '&':
                if self.peek() == '&':
                    self.advance()
                    self.advance()
                    return {'token': 'AND', 'tokenText': '&&'}
                else:
                    self.error("Invalid character: &")
            # ||
            if self.current_char == '|':
                if self.peek() == '|':
                    self.advance()
                    self.advance()
                    return {'token': 'OR', 'tokenText': '||'}
                else:
                    self.error("Invalid character: |")
             # identifiers or keywords.
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            # numeric constants [integer or floating point]
            if self.current_char.isdigit():
                return self.number()

            # if the character doesnt match any known token
            self.error(f"Unknown character: {self.current_char}")

        # EOF
        return {'token': 'DD', 'tokenText': '$$'}

lexer = None

# initLexer
# accepts a string(filename) with the src code to analyze
# opens file then create buffer(self.text) for the file to be compiled
# returns True(file open succeeded) or False(file open fail)
def initLexer(filename):
    global lexer
    try:
        lexer = Lexer(filename)
        return True
    except IOError:
        return False
    
# getNextToken
# scan the text and return information for the next token
# Returns the next token from the lexer
def getNextToken():
    global lexer
    if lexer is None:
        raise Exception("Lexer not initialized. Call initLexer(filename) first.")
    return lexer.getNextToken()

# main (for standalone testing)
def main():
    # src file check
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    if not initLexer(filename):
        print("Failed to open file:", filename)
        sys.exit(1)

    # retrieve and print tokens until DD(EOf)
    token = getNextToken()
    while token['token'] != 'DD':
        print("token: {} : |{}|".format(token['token'], token['tokenText']))
        token = getNextToken()
    print("token: DD : ||")

if __name__ == '__main__':
    main()
