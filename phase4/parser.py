import sys
from lexer import getNextToken
from stm import SymbolTableManager
from compiler import IRCode, ExprAttr

class Parser:
    def __init__(self):
        self.current = getNextToken()
        self.symtab  = SymbolTableManager()
        self.IR      = IRCode()
        self.globals    = {}      
        self.in_global  = False  
        self.functions = set()

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

    # Program => decllist funcdecls DD
    def parse_Program(self):
        self.IR.emit_data_segment()

        self.in_global = True
        self.parse_decllist()
        self.in_global = False

        self.IR.emit_text_segment()
        self.parse_funcdecls()
        self.match("DD")

    # funcdecls => funcdecl funcdecls | maindecl
    def parse_funcdecls(self):
        if self.peek() == "FUNCTION":
            self.parse_funcdecl()
            self.parse_funcdecls()
        elif self.peek() == "MAIN":
            self.parse_maindecl()

    # funcdecl => FUNCTION ftypespec simplevar fdeclparms LBRACE decllist statementlist RBRACE
    def parse_funcdecl(self):
        self.match("FUNCTION")
        ret_type = self.parse_ftypespec()
        fname = self.current['tokenText']
        self.functions.add(fname)
        self.match("ID")
        self.IR.emit('.label', 0, 0, fname)

        # enter function scope 
        self.symtab.enterScope()
        self.symtab.addSymbol(fname, ret_type, memory_location=fname)
        self.parse_fdeclparms()
        self.match("LBRACE")
        self.parse_decllist()
        self.parse_statementlist()
        self.match("RBRACE")

        # exit function scope
        self.symtab.exitScope()
        self.IR.emit('return', 0, 0, 0)

    # maindecl => MAIN LPAREN RPAREN LBRACE decllist statementlist RBRACE
    def parse_maindecl(self):
        self.match("MAIN")
        self.match("LPAREN")
        self.match("RPAREN")
        self.IR.emit('.label', 0, 0, 'main')
        # enter main scope
        self.symtab.enterScope()

        self.match("LBRACE")
        self.parse_decllist()
        self.parse_statementlist()
        self.match("RBRACE")

        # exit main scope
        self.symtab.exitScope()
        self.IR.emit('halt', 0, 0, 0) # last instruction before exiting

    # ftypespec => VOID | INT | FLOAT
    def parse_ftypespec(self):
        if self.peek() in ("VOID", "INT", "FLOAT"):
            typ = self.peek()
            self.match(typ)
            return typ
        self.error("Expected VOID, INT, or FLOAT in ftypespec")

    # fdeclparms => LPAREN fparmlist RPAREN
    def parse_fdeclparms(self):
        self.match("LPAREN")
        self.parse_fparmlist()
        self.match("RPAREN")

    # fparmlist => fparm fparmlistrem | eps
    def parse_fparmlist(self):
        if self.peek() in ("INT", "FLOAT"):
            self.parse_fparm()
            self.parse_fparmlistrem()

    # fparmlistrem => COMMA fparm fparmlistrem | eps
    def parse_fparmlistrem(self):
        if self.peek() == "COMMA":
            self.match("COMMA")
            self.parse_fparm()
            self.parse_fparmlistrem()

    # fparm => typespec parmVar
    def parse_fparm(self):
        typ = self.parse_typespec()
        name = self.current['tokenText']
        self.match("ID")
        if self.peek() == "LBRACKET":
            self.match("LBRACKET"); self.match("RBRACKET")
        self.symtab.addSymbol(name, typ, memory_location=name)

    # parmVar => ID parmVarTail
    def parse_parmVar(self):
        self.match("ID")
        self.parse_parmVarTail()

    # parmVarTail => LBRACKET RBRACKET parmVarTail | eps
    def parse_parmVarTail(self):
        if self.peek() == "LBRACKET":
            self.match("LBRACKET"); self.match("RBRACKET")
            self.parse_parmVarTail()

    # decllist => decl decllist | eps
    def parse_decllist(self):
        if self.peek() in ("INT", "FLOAT"):
            self.parse_decl()
            self.parse_decllist()

    # decl => typespec variablelist SEMICOLON
    def parse_decl(self):
        typ = self.current['token']
        self.parse_typespec()
        vars = self.parse_variablelist()
        self.match("SEMICOLON")
        directive = '.int' if typ=='INT' else '.float'
        for name,count in vars:
            self.symtab.addSymbol(name, typ, memory_location=name)
            self.IR.emit_data_directive(directive, count, name)
            if self.in_global:
                self.globals[name] = (typ, name)

    # variablelist => variable variablelisttail
    def parse_variablelist(self):
        lst = []
        name,count = self.parse_variable()
        lst.append((name,count))
        lst.extend(self.parse_variablelisttail())
        return lst

    # variablelisttail => COMMA variable variablelisttail | eps
    def parse_variablelisttail(self):
        if self.peek() == "COMMA":
            self.match("COMMA")
            name,count = self.parse_variable()
            return [(name,count)] + self.parse_variablelisttail()
        return []

    # variable => ID variabletail
    def parse_variable(self):
        name = self.current['tokenText']
        self.match("ID")
        # for each “[N]” multiply count by N
        count = 1
        while self.peek() == "LBRACKET":
            self.match("LBRACKET")
            size = int(self.current["tokenText"])
            self.match("ICONST")
            self.match("RBRACKET")
            count *= size
        return name, count


    # variabletail => LBRACKET ICONST RBRACKET variabletail | eps
    def parse_variabletail(self):
        if self.peek() == "LBRACKET":
            self.match("LBRACKET"); self.match("ICONST"); self.match("RBRACKET")
            self.parse_variabletail()

    # typespec => INT | FLOAT
    def parse_typespec(self):
        if self.peek() in ("INT","FLOAT"):
            self.match(self.peek())
        else:
            self.error("Expected INT or FLOAT in typespec")

    # bstatementlist => LBRACE statementlist RBRACE
    def parse_bstatementlist(self):
        self.match("LBRACE")
        # block scope
        self.symtab.enterScope()
        self.parse_statementlist()
        self.symtab.exitScope()
        self.match("RBRACE")

    # statementlist => statement statementlisttail | eps
    def parse_statementlist(self):
        if self.peek() in ("WHILE","IF","ID","PRINT","READ","RETURN","CALL"):
            self.parse_statement()
            self.parse_statementlisttail()

    # statementlisttail => SEMICOLON statementlist | eps
    def parse_statementlisttail(self):
        if self.peek() == "SEMICOLON":
            self.match("SEMICOLON")
            self.parse_statementlist()

    # statement => whilestatement | ifstatement | assignmentstatement | printstatement | readstatement | returnstatement | callstatement
    def parse_statement(self):
        tok = self.peek()
        if tok == "WHILE": self.parse_whilestatement()
        elif tok == "IF": self.parse_ifstatement()
        elif tok == "ID": self.parse_assignmentstatement()
        elif tok == "PRINT": self.parse_printstatement()
        elif tok == "READ": self.parse_readstatement()
        elif tok == "RETURN": self.parse_returnstatement()
        elif tok == "CALL": self.parse_callstatement()
        else: self.error("Expected statement")

    # whilestatement => WHILE relationalexpr bstatementlist
    def parse_whilestatement(self):
        self.match("WHILE")
        self.match("LPAREN")
        cond = self.parse_relationalexpr()
        self.match("RPAREN")
        start=self.IR.new_label(); end=self.IR.new_label()
        self.IR.emit('.label',0,0,start)
        self.IR.emit('beq',cond.location,0,end)
        self.parse_bstatementlist()
        self.IR.emit('j',0,0,start)
        self.IR.emit('.label',0,0,end)

    # ifstatement => IF relationalexpr bstatementlist istail
    def parse_ifstatement(self):
        self.match("IF")
        self.match("LPAREN")
        cond = self.parse_relationalexpr()
        self.match("RPAREN")
        # for or && after the first conditional
        while self.peek() in ("OR","AND"):
            op = self.current["token"]
            self.match(op)
            self.match("LPAREN")
            right = self.parse_relationalexpr()
            self.match("RPAREN")

            # fold into one boolean temp
            temp = self.IR.new_temp()
            instr = "or" if op=="OR" else "and"
            self.IR.emit(instr, cond.location, right.location, temp)
            cond = ExprAttr("INT", temp)
        els=self.IR.new_label(); end=self.IR.new_label()
        self.IR.emit('beq',cond.location,0,els)
        self.parse_bstatementlist()
        self.IR.emit('j',0,0,end)
        self.IR.emit('.label',0,0,els)
        self.parse_istail()
        self.IR.emit('.label',0,0,end)

    # istail => ELSE bstatementlist | eps
    def parse_istail(self):
        if self.peek() == "ELSE":
            self.match("ELSE")
            self.parse_bstatementlist()

    # assignmentstatement => usevariable ASSIGN otherexpression SEMICOLON
    def parse_assignmentstatement(self):
        lhs=self.parse_usevariable()
        self.match('ASSIGN')
        rhs=self.parse_otherexpression()
        op='sw' if rhs.type=='INT' else 'fsw'
        self.IR.emit(op,rhs.location,0,lhs.location)

    # printstatement => PRINT otherexpression SEMICOLON
    def parse_printstatement(self):
        self.match('PRINT')
        expr=self.parse_otherexpression()
        trap=2 if expr.type=='INT' else 4
        self.IR.emit('syscall',trap,expr.location,0)

    # readstatement => READ usevariable SEMICOLON
    def parse_readstatement(self):
        self.match('READ')
        lhs=self.parse_usevariable()
        trap=1 if lhs.type=='INT' else 3
        tmp=self.IR.new_temp() if lhs.type=='INT' else self.IR.new_ftemp()
        self.IR.emit('syscall',trap,tmp,0)
        self.IR.emit('sw' if lhs.type=='INT' else 'fsw',tmp,0,lhs.location)

    # returnstatement => RETURN [otherexpression] SEMICOLON
    def parse_returnstatement(self):
        self.match('RETURN')
        if self.peek() in ('ID','ICONST','FCONST','LPAREN','MINUS'):
            expr=self.parse_otherexpression()
            self.IR.emit('return',expr.location,0,0)

    # callstatement => CALL ID LPAREN [args] RPAREN SEMICOLON
    def parse_callstatement(self):
        self.match('CALL')
        fname=self.current['tokenText']; self.match('ID')
        self.match('LPAREN')
        args=[]
        if self.peek() != 'RPAREN':
            expr=self.parse_otherexpression(); args.append(expr)
            while self.peek()==',': self.match(','); expr=self.parse_otherexpression(); args.append(expr)
        self.match('RPAREN')
        for arg in args: self.IR.emit('param',arg.location,0,0)
        self.IR.emit('call',fname,len(args),0)

    # otherexpression => term otherexpressiontail
    def parse_otherexpression(self):
        left=self.parse_term()
        return self.parse_otherexpressiontail(left)

    def parse_otherexpressiontail(self,left_attr):
        if self.peek() in ('PLUS','MINUS'):
            op=self.current['token']; self.match(op)
            right=self.parse_term()
            if left_attr.type != right.type:
                if left_attr.type=='INT': tmp=self.IR.new_ftemp(); self.IR.emit('tf',left_attr.location,0,tmp); left_attr=ExprAttr('FLOAT',tmp)
                else: tmp=self.IR.new_ftemp(); self.IR.emit('tf',right.location,0,tmp); right=ExprAttr('FLOAT',tmp)
            instr='add' if op=='PLUS' else 'sub'
            if left_attr.type=='FLOAT': instr='f'+instr; dest=self.IR.new_ftemp()
            else: dest=self.IR.new_temp()
            self.IR.emit(instr,left_attr.location,right.location,dest)
            return self.parse_otherexpressiontail(ExprAttr(left_attr.type,dest))
        return left_attr

    def parse_term(self):
        left=self.parse_factor()
        return self.parse_termtail(left)

    def parse_termtail(self,left_attr):
        if self.peek() in ('MULT','DIV'):
            op=self.current['token']; self.match(op)
            right=self.parse_factor()
            if left_attr.type != right.type:
                if left_attr.type=='INT': tmp=self.IR.new_ftemp(); self.IR.emit('tf',left_attr.location,0,tmp); left_attr=ExprAttr('FLOAT',tmp)
                else: tmp=self.IR.new_ftemp(); self.IR.emit('tf',right.location,0,tmp); right=ExprAttr('FLOAT',tmp)
            instr='mul' if op=='MULT' else 'div'
            if left_attr.type=='FLOAT': instr='f'+instr; dest=self.IR.new_ftemp()
            else: dest=self.IR.new_temp()
            self.IR.emit(instr,left_attr.location,right.location,dest)
            return self.parse_termtail(ExprAttr(left_attr.type,dest))
        return left_attr

    def parse_factor(self):
        tok = self.peek()
    
        # function‐call expression
        if tok == 'ID' and self.current['tokenText'] in self.functions:
            fname = self.current['tokenText']
            self.match('ID')
            self.match('LPAREN')
            args = []
            if self.peek() != 'RPAREN':
                args.append(self.parse_otherexpression())
                while self.peek() == 'COMMA':
                    self.match('COMMA')
                    args.append(self.parse_otherexpression())
            self.match('RPAREN')
    
            for arg in args:
                self.IR.emit('param', arg.location, 0, 0)
            ret = self.IR.new_temp()
            self.IR.emit('call', fname, len(args), ret)
            return ExprAttr('INT', ret)
    
        # variable reference
        if tok == 'ID':
            return self.parse_usevariable()
    
        # integer literal
        if tok == 'ICONST':
            val = int(self.current['tokenText'])
            self.match('ICONST')
            temp = self.IR.new_temp()
            self.IR.emit('li', val, 0, temp)
            return ExprAttr('INT', temp)
    
        # float literal
        if tok == 'FCONST':
            val = float(self.current['tokenText'])
            self.match('FCONST')
            temp = self.IR.new_ftemp()
            self.IR.emit('fl', val, 0, temp)
            return ExprAttr('FLOAT', temp)
    
        # parenthesized sub‐expression
        if tok == 'LPAREN':
            self.match('LPAREN')
            expr = self.parse_otherexpression()
            self.match('RPAREN')
            return expr
    
        # unary minus
        if tok == 'MINUS':
            self.match('MINUS')
            expr = self.parse_factor()
            instr = 'sub' if expr.type == 'INT' else 'fsub'
            # choose the right temp based on type
            dest = (self.IR.new_temp() if expr.type == 'INT'
                    else self.IR.new_ftemp())
            self.IR.emit(instr, 0, expr.location, dest)
            return ExprAttr(expr.type, dest)
        self.error("Expected factor")
    
    def parse_usevariable(self):
        name = self.current['tokenText']
        self.match('ID')

        # local lookup
        sym = self.symtab.lookup(name)
        # undeclared variable
        if sym is None:
            self.error(f"Undeclared variable {name}")
        # array indexing
        if self.peek()=='LBRACKET':
            self.match('LBRACKET')
            idx = self.parse_otherexpression()
            self.match('RBRACKET')

            # pick the right storage
            if sym is None and name in self.globals:
                typ, mem_loc = self.globals[name]
            else:
                typ, mem_loc = sym.type, sym.memory_location

            # base address
            base = self.IR.new_temp()
            self.IR.emit('la', mem_loc, 0, base)

            # scaled offset
            off = self.IR.new_temp()
            self.IR.emit('mul', idx.location, 4, off)

            addr = self.IR.new_temp()
            self.IR.emit('add', base, off, addr)

        else:
            # simple variable
            if sym is None and name in self.globals:
                typ, mem_loc = self.globals[name]
            else:
                typ, mem_loc = sym.type, sym.memory_location

            addr = self.IR.new_temp()
            self.IR.emit('la', mem_loc, 0, addr)

        # load from addr into a value temp
        if typ == 'INT':
            val = self.IR.new_temp()
            self.IR.emit('lw', addr, 0, val)
        else:
            val = self.IR.new_ftemp()
            self.IR.emit('flw', addr, 0, val)

        return ExprAttr(typ, val)

    def parse_relationalexpr(self):
        # a in a == b
        left = self.parse_otherexpression()
        # Relational operators including NOTEQUAL
        while self.peek() in ('LT','LE','GT','GE','EQUAL','NOTEQUAL'):
            op = self.current['token']
            self.match(op)
            right = self.parse_otherexpression()
            dest = self.IR.new_temp()
            # map NOTEQUAL to 'ne'
            instr = op.lower() if op != 'NOTEQUAL' else 'ne'
            self.IR.emit(instr, left.location, right.location, dest)
            left = ExprAttr('INT', dest)
        # Boolean chaining: AND / OR
        while self.peek() in ('AND', 'OR'):
            op = self.current['token']
            self.match(op)
            right = self.parse_relationalexpr()
            dest = self.IR.new_temp()
            instr = 'and' if op == 'AND' else 'or'
            self.IR.emit(instr, left.location, right.location, dest)
            left = ExprAttr('INT', dest)
        return left
