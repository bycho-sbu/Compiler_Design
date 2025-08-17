import sys
from lexer import getNextToken

class Parser:
    def __init__(self):
        # lookahead
        self.current = getNextToken()

    def error(self, msg):
        print(f"Parse error: {msg}, got {self.current['token']}")
        sys.exit(1)

    def peek(self):
        return self.current['token']

    def match(self, token_type):
        if self.current['token'] == token_type:
            self.current = getNextToken()
        else:
            self.error(f"Expected {token_type}")

    def trace(self, production):
        print(production)

    # Program => decllist funcdecls DD
    def parse_Program(self):
        self.trace("Parsing program: ")
        self.trace("Program => decllist funcdecls DD")
        self.parse_decllist()
        self.parse_funcdecls()
        self.match("DD")

    # funcdecls => funcdecl funcdecls | maindecl
    def parse_funcdecls(self):
        if self.peek() == "FUNCTION":
            self.trace("funcdecls => funcdecl funcdecls")
            self.parse_funcdecl()
            self.parse_funcdecls()
        elif self.peek() == "MAIN":
            self.trace("funcdecls => maindecl")
            self.parse_maindecl()
        else:
            self.error("Expected FUNCTION or MAIN in funcdecls")

    # funcdecl => FUNCTION ftypespec simplevar fdeclparms LBRACE decllist statementlist RBRACE
    def parse_funcdecl(self):
        self.trace("funcdecl => FUNCTION ftypespec simplevar fdeclparms LBRACE decllist statementlist RBRACE")
        self.match("FUNCTION")
        self.parse_ftypespec()
        self.match("ID")                  # simplevar
        self.parse_fdeclparms()
        self.match("LBRACE")
        self.parse_decllist()
        self.parse_statementlist()
        self.match("RBRACE")

    # maindecl => MAIN LPAREN RPAREN LBRACE decllist statementlist RBRACE
    def parse_maindecl(self):
        self.trace("maindecl => MAIN LPAREN RPAREN LBRACE decllist statementlist RBRACE")
        self.match("MAIN")
        self.match("LPAREN")
        self.match("RPAREN")
        self.match("LBRACE")
        self.parse_decllist()
        self.parse_statementlist()
        self.match("RBRACE")

    # ftypespec => VOID | INT | FLOAT
    def parse_ftypespec(self):
        if self.peek() in ("VOID", "INT", "FLOAT"):
            self.trace(f"ftypespec => {self.peek()}")
            self.match(self.peek())
        else:
            self.error("Expected VOID, INT, or FLOAT in ftypespec")

    # fdeclparms => LPAREN fparmlist RPAREN
    def parse_fdeclparms(self):
        self.trace("fdeclparms => LPAREN fparmlist RPAREN")
        self.match("LPAREN")
        self.parse_fparmlist()
        self.match("RPAREN")

    # fparmlist => fparm fparmlistrem | eps
    def parse_fparmlist(self):
        if self.peek() in ("INT", "FLOAT"):
            self.trace("fparmlist => fparm fparmlistrem")
            self.parse_fparm()
            self.parse_fparmlistrem()
        else:
            self.trace("fparmlist => eps")

    # fparm => typespec parmVar
    def parse_fparm(self):
        self.trace("fparm => typespec parmVar")
        self.parse_typespec()
        self.parse_parmVar()    

    # parmVar => ID parmVarTail
    def parse_parmVar(self):
        self.trace("parmVar => ID parmVarTail")
        self.match("ID")
        self.parse_parmVarTail()     

    # parmVarTail => LBRACKET RBRACKET parmVarTail | eps
    def parse_parmVarTail(self):
        if self.peek() == "LBRACKET":
            self.trace("parmVarTail => LBRACKET RBRACKET parmVarTail")
            self.match("LBRACKET")
            self.match("RBRACKET")
            self.parse_parmVarTail()
        else:
            self.trace("parmVarTail => eps")

    # fparmlistrem => COMMA fparm fparmlistrem | eps
    def parse_fparmlistrem(self):
        if self.peek() == "COMMA":
            self.trace("fparmlistrem => COMMA fparm fparmlistrem")
            self.match("COMMA")
            self.parse_fparm()
            self.parse_fparmlistrem()
        else:
            self.trace("fparmlistrem => eps")

    # decllist => decl decllist | eps
    def parse_decllist(self):
        if self.peek() in ("INT", "FLOAT"):
            self.trace("decllist => decl decllist")
            self.parse_decl()
            self.parse_decllist()
        else:
            self.trace("decllist => eps")

    # bstatementlist => LBRACE statementlist RBRACE
    def parse_bstatementlist(self):
        self.trace("bstatementlist => LBRACE statementlist RBRACE")
        self.match("LBRACE")
        self.parse_statementlist()
        self.match("RBRACE")

    # statementlist => statement statementlisttail  
    def parse_statementlist(self):
        if self.peek() in ("WHILE","IF","ID","PRINT","READ","RETURN","CALL"):
            self.trace("statementlist => statement statementlisttail")
            self.parse_statement()
            self.parse_statementlisttail()
        else:
            self.trace("statementlist => eps")

    # statementlisttail => SEMICOLON statementlist | eps
    def parse_statementlisttail(self):
        if self.peek() == "SEMICOLON":
            self.trace("statementlisttail => SEMICOLON statementlist")
            self.match("SEMICOLON")
            self.parse_statementlist()
        else:
            self.trace("statementlisttail => eps")

    # decl => typespec variablelist
    def parse_decl(self):
        self.trace("decl => typespec variablelist")
        self.parse_typespec()
        self.parse_variablelist()
        self.match("SEMICOLON")

    # variablelist => variable variablelisttail
    def parse_variablelist(self):
        self.trace("variablelist => variable variablelisttail")
        self.parse_variable()
        self.parse_variablelisttail()
    # variablelisttail => COMMA variable variablelisttail | SEMICOLON
    def parse_variablelisttail(self):
        if self.peek() == "COMMA":
            self.trace("variablelisttail => COMMA variable variablelisttail")
            self.match("COMMA")
            self.parse_variable()
            self.parse_variablelisttail()
        elif self.peek() == "SEMICOLON":
            self.trace("variablelisttail => SEMICOLON")
            return
        else:
            self.error("Expected COMMA or SEMICOLON in variablelisttail")


    # variable => ID variabletail
    def parse_variable(self):
        self.trace("variable => ID variabletail")
        self.match("ID")
        self.parse_variabletail()

    # variabletail => LBRACKET ICONST RBRACKET variabletail | eps
    def parse_variabletail(self):
        if self.peek() == "LBRACKET":
            self.trace("variabletail => LBRACKET ICONST RBRACKET variabletail")
            self.match("LBRACKET")
            self.match("ICONST")
            self.match("RBRACKET")
            self.parse_variabletail()
        else:
            self.trace("variabletail => eps")

    # typespec => INT | FLOAT
    def parse_typespec(self):
        if self.peek() in ("INT", "FLOAT"):
            self.trace(f"typespec => {self.peek()}")
            self.match(self.peek())
        else:
            self.error("Expected INT or FLOAT in typespec")
    
     # usevariable => ID usevariabletail
    def parse_usevariable(self):
        self.trace("usevariable => ID usevariabletail")
        self.match("ID")
        self.parse_usevariabletail()

    # usevariabletail => arraydim | eps
    def parse_usevariabletail(self):
        if self.peek() == "LBRACKET":
            self.trace("usevariabletail => arraydim")
            self.parse_arraydim()
        else:
            self.trace("usevariabletail => eps")

    # arraydim => LBRACKET arraydimtail
    def parse_arraydim(self):
       if self.peek() == "LBRACKET":
           self.trace("arraydim => LBRACKET arraydimtail")
           self.match("LBRACKET")
           self.parse_arraydimtail()
       else:
           self.trace("arraydim => eps")

    # arraydimtail => ICONST RBRACKET arraydim | ID RBRACKET arraydim
    def parse_arraydimtail(self):
        if self.peek() == "ICONST":
            self.trace("arraydimtail => ICONST RBRACKET arraydim")
            self.match("ICONST")
            self.match("RBRACKET")
            self.parse_arraydim()
        elif self.peek() == "ID":
            self.trace("arraydimtail => ID RBRACKET arraydim")
            self.match("ID")
            self.match("RBRACKET")
            self.parse_arraydim()
        else:
            self.error("Expected ICONST or ID in arraydimtail")


    # statement => whilestatement | ifstatement | assignmentstatement | printstatement | readstatement | returnstatement | callstatement
    def parse_statement(self):
        tok = self.peek()
        if tok == "WHILE":
            self.trace("statement => whilestatement")
            self.parse_whilestatement()
        elif tok == "IF":
            self.trace("statement => ifstatement")
            self.parse_ifstatement()
        elif tok == "ID":
            self.trace("statement => assignmentstatement")
            self.parse_assignmentstatement()
        elif tok == "PRINT":
            self.trace("statement => printstatement")
            self.parse_printstatement()
        elif tok == "READ":
            self.trace("statement => readstatement")
            self.parse_readstatement()
        elif tok == "RETURN":
            self.trace("statement => returnstatement")
            self.parse_returnstatement()
        elif tok == "CALL":
            self.trace("statement => callstatement")
            self.parse_callstatement()
        else:
            self.error("Expected statement")

    # basicexpr => basicterm basicexprtail
    def parse_basicexpr(self):
        self.trace("basicexpr => basicterm basicexprtail")
        self.parse_basicterm()
        self.parse_basicexprtail()

    # basicexprtail => PLUS basicterm basicexprtail | MINUS basicterm basicexprtail | eps
    def parse_basicexprtail(self):
        if self.peek() == "PLUS":
            self.trace("basicexprtail => PLUS basicterm basicexprtail")
            self.match("PLUS")
            self.parse_basicterm()
            self.parse_basicexprtail()
        elif self.peek() == "MINUS":
            self.trace("basicexprtail => MINUS basicterm basicexprtail")
            self.match("MINUS")
            self.parse_basicterm()
            self.parse_basicexprtail()
        else:
            self.trace("basicexprtail => eps")

    # basicterm => basicfactor basictermtail
    def parse_basicterm(self):
        self.trace("basicterm => basicfactor basictermtail")
        self.parse_basicfactor()
        self.parse_basictermtail()

    # basictermtail => MULT basicfactor basictermtail | DIV basicfactor basictermtail | eps
    def parse_basictermtail(self):
        if self.peek() == "MULT":
            self.trace("basictermtail => MULT basicfactor basictermtail")
            self.match("MULT")
            self.parse_basicfactor()
            self.parse_basictermtail()
        elif self.peek() == "DIV":
            self.trace("basictermtail => DIV basicfactor basictermtail")
            self.match("DIV")
            self.parse_basicfactor()
            self.parse_basictermtail()
        else:
            self.trace("basictermtail => eps")

    # basicfactor => ID | ICONST
    def parse_basicfactor(self):
        if self.peek() == "ID":
            self.trace("basicfactor => ID")
            self.match("ID")
        elif self.peek() == "ICONST":
            self.trace("basicfactor => ICONST")
            self.match("ICONST")
        else:
            self.error("Expected ID or ICONST in basicfactor")

    # assignmentstatement => usevariable ASSIGN otherexpression
    def parse_assignmentstatement(self):
        self.trace("assignmentstatement => usevariable ASSIGN otherexpression")
        self.parse_usevariable()
        self.match("ASSIGN")
        self.parse_otherexpression()

    # otherexpression => term otherexpressiontail
    def parse_otherexpression(self):
        self.trace("otherexpression => term otherexpressiontail")
        self.parse_term()
        self.parse_otherexpressiontail()

    # otherexpressiontail => PLUS term otherexpressiontail | MINUS term otherexpressiontail | eps 
    def parse_otherexpressiontail(self):
        if self.peek() == "PLUS":
            self.trace("otherexpressiontail => PLUS term otherexpressiontail")
            self.match("PLUS")
            self.parse_term()
            self.parse_otherexpressiontail()
        elif self.peek() == "MINUS":
            self.trace("otherexpressiontail => MINUS term otherexpressiontail")
            self.match("MINUS")
            self.parse_term()
            self.parse_otherexpressiontail()
        else:
            self.trace("otherexpressiontail => eps")
    # term => factor termtail   
    def parse_term(self):
        self.trace("term => factor termtail")
        self.parse_factor()
        self.parse_termtail()

    # termtail => MULT factor termtail | DIV factor termtail  | eps   
    def parse_termtail(self):
        if self.peek() == "MULT":
            self.trace("termtail => MULT factor termtail")
            self.match("MULT")
            self.parse_factor()
            self.parse_termtail()
        elif self.peek() == "DIV":
            self.trace("termtail => DIV factor termtail")
            self.match("DIV")
            self.parse_factor()
            self.parse_termtail()
        else:
            self.trace("termtail => eps")

    # factortail => usevariabletail | funccalltail
    def parse_factortail(self):
        if self.peek() == "LBRACKET":
            self.trace("factortail => usevariabletail")
            self.parse_usevariabletail()
        elif self.peek() == "LPAREN":
            self.trace("factortail => funccalltail")
            self.parse_funccalltail()
        else:
            self.trace("factortail => eps")

    # funccalltail => LPAREN arglist RPAREN
    def parse_funccalltail(self):
        self.trace("funccalltail => LPAREN arglist RPAREN")
        self.match("LPAREN")
        self.parse_arglist()
        self.match("RPAREN")

    # arglist => otherexpression arglistrem | eps
    def parse_arglist(self):
        if self.peek() in ("ID", "ICONST", "FCONST", "LPAREN", "MINUS"):
            self.trace("arglist => otherexpression arglistrem")
            self.parse_otherexpression()
            self.parse_arglistrem()
        else:
            self.trace("arglist => eps")
    # arglistrem => COMMA otherexpression arglistrem | eps
    def parse_arglistrem(self):
        if self.peek() == "COMMA":
            self.trace("arglistrem => COMMA otherexpression arglistrem")
            self.match("COMMA")
            self.parse_otherexpression()
            self.parse_arglistrem()
        else:
            self.trace("arglistrem => eps")

    # factor => ID factortail | ICONST | FCONST | LPAREN otherexpression RPAREN | MINUS factor
    def parse_factor(self):
        tok = self.peek()
        if tok == "ID":
            self.trace("factor => ID factortail")
            self.match("ID")
            self.parse_factortail()
        elif tok == "ICONST":
            self.trace("factor => ICONST")
            self.match("ICONST")
        elif tok == "FCONST":
            self.trace("factor => FCONST")
            self.match("FCONST")
        elif tok == "LPAREN":
            self.trace("factor => LPAREN otherexpression RPAREN")
            self.match("LPAREN")
            self.parse_otherexpression()
            self.match("RPAREN")
        elif tok == "MINUS":
            self.trace("factor => MINUS factor")
            self.match("MINUS")
            self.parse_factor()
        else:
            self.error("Expected factor")

    # whilestatement => WHILE relationalexpr bstatementlist
    def parse_whilestatement(self):
        self.trace("whilestatement => WHILE relationalexpr bstatementlist")
        self.match("WHILE")
        self.parse_relationalexpr()
        self.parse_bstatementlist()

    # ifstatement => IF relationalexpr bstatementlist istail
    def parse_ifstatement(self):
        self.trace("ifstatement => IF relationalexpr bstatementlist istail")
        self.match("IF")
        self.parse_relationalexpr()
        self.parse_bstatementlist()
        self.parse_istail()

    # istail => ELSE bstatementlist | eps
    def parse_istail(self):
        if self.peek() == "ELSE":
            self.trace("Istail => ELSE bstatementlist")
            self.match("ELSE")
            self.parse_bstatementlist()
        else:
            self.trace("Istail => eps")

    # relationalexpr => condexpr relationalexprtail
    def parse_relationalexpr(self):
        self.trace("relationalexpr => condexpr relationalexprtail")
        self.parse_condexpr()
        self.parse_relationalexprtail()

    # relationalexprtail => AND condexpr | OR condexpr | eps
    def parse_relationalexprtail(self):
        if self.peek() == "AND":
            self.trace("relationalexprtail => AND condexpr")
            self.match("AND")
            self.parse_condexpr()
        elif self.peek() == "OR":
            self.trace("relationalexprtail => OR condexpr")
            self.match("OR")
            self.parse_condexpr()
        else:
            self.trace("relationalexprtail => eps")

    # condexpr => LPAREN otherexpression condexprtail RPAREN | otherexpression condexprtail | NOT condexpr
    def parse_condexpr(self):
        if self.peek() == "LPAREN":
            self.trace("condexpr => LPAREN otherexpression condexprtail RPAREN")
            self.match("LPAREN")
            self.parse_otherexpression()
            self.parse_condexprtail()
            self.match("RPAREN")
        elif self.peek() == "NOT":
            self.trace("condexpr => NOT condexpr")
            self.match("NOT")
            self.parse_condexpr()
        else:
            self.trace("condexpr => otherexpression condexprtail")
            self.parse_otherexpression()
            self.parse_condexprtail()

        # condexprtail => LT otherexpression | LE otherexpression | GT otherexpression | GE otherexpression | EQUAL otherexpression | eps
    def parse_condexprtail(self):
        if self.peek() == "LT":
            self.trace("condexprtail => LT otherexpression")
            self.match("LT")
            self.parse_otherexpression()
        elif self.peek() == "LE":
            self.trace("condexprtail => LE otherexpression")
            self.match("LE")
            self.parse_otherexpression()
        elif self.peek() == "GT":
            self.trace("condexprtail => GT otherexpression")
            self.match("GT")
            self.parse_otherexpression()
        elif self.peek() == "GE":
            self.trace("condexprtail => GE otherexpression")
            self.match("GE")
            self.parse_otherexpression()
        elif self.peek() == "EQUAL":
            self.trace("condexprtail => EQUAL otherexpression")
            self.match("EQUAL")
            self.parse_otherexpression()
        else:
            self.trace("condexprtail => eps")

    # printstatement => PRINT otherexpression
    def parse_printstatement(self):
        self.trace("printstatement => PRINT otherexpression")
        self.match("PRINT")
        self.parse_otherexpression()

    # readstatement => READ usevariable
    def parse_readstatement(self):
        self.trace("readstatement => READ usevariable")
        self.match("READ")
        self.parse_usevariable()

    # returnstatement => RETURN otherexpression | RETURN
    def parse_returnstatement(self):
        self.match("RETURN")
        if self.peek() in ("ID","ICONST","FCONST","LPAREN","MINUS"):
            self.trace("returnstatement => RETURN otherexpression")
            self.parse_otherexpression()
        else:
            self.trace("returnstatement => RETURN")

    # callstatement => CALL ID funccalltail
    def parse_callstatement(self):
        self.trace("callstatement => CALL ID funccalltail")
        self.match("CALL")
        self.match("ID")
        self.parse_funccalltail()

    
