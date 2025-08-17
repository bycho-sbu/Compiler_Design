# stm.py Symbol Table Manager 

class SymbolInfo:
    """
    hold identifier(array of ch or str) : str
    hold a set of attrbiutes appropriate about the identifier : dict
    type field   : str
    mem location : num
    """

    def __init__(self, identifier, type, memory_location):
        self.identifier = identifier   
        self.type = type
        self.memory_location = memory_location
        self.attributes = {}            
        
    # human readable
    def __str__(self):
        # default information of the symbol(identifier, type, memory address)
        details = {
            "identifier": self.identifier,
            "type": self.type,
            "memory_location": self.memory_location
        }
        # some attrbiutes that will be added
        details.update(self.attributes)
        return f"SymbolInfo(details={details})"

class SymbolTableManager:
    def __init__(self):
        self.initSymTab()

    def initSymTab(self):
        self.symbol_table = {0: {}} # container for all symbols, global with key 0
        self.current_scope = 0      # holds the identifier in the active scope
        self.scope_stack = [0]      # stack to store scopes
        self.last_scope = 0         # last used scope 

    def enterScope(self):
        """
        enters new scope +1
        all symbols added will be defined in the scope until exitScope()
        returns id of the new scope
        scopes asigned monotonically increasing seq
        0 = global scope
        each new function definition increments last used scope number
        returns:
            last used scope number
        """
        self.last_scope += 1
        new_scope = self.last_scope
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        self.symbol_table[new_scope] = {}
        return new_scope

    def exitScope(self):
        """
        reverts current scope to the global scope 0 
        only resetting the current scope to global no removal from the table
        """
        if len(self.scope_stack) > 1:
            self.scope_stack.pop() # exit the current scope
            self.current_scope = self.scope_stack[-1]  # current scope replaced by top stack
        else:
            self.current_scope = 0

    def addSymbol(self, identifier, type=None, memory_location=None):
        """
        adds a Symbolinfo record to the table
        only contain the identifier at init
        minimial information added to the current scope
        should override the the attributes 
        returns:
            bool: True if the symbol is added to the table, 
                  False if it already exists in the current scope
        """
        scope = self.current_scope
        # symbol already exists in this scope
        if identifier in self.symbol_table[scope]:
            return False  
        symbol = SymbolInfo(identifier, type, memory_location)
        self.symbol_table[scope][identifier] = symbol
        return True

    def addAttributeToSymbol(self, identifier, scope, attribute, value):
        """
        locates the identifier in the requested scope
        adds an attribute for the symbol identified by 'identifier'
        in the given scope
        returns:
            bool: True on success, False if the symbol isn't found
        """
        # symbol doesnt exist
        if scope not in self.symbol_table or identifier not in self.symbol_table[scope]:
            return False
        
        symbol = self.symbol_table[scope][identifier]

        # update attribute within the dictionary
        symbol.attributes[attribute] = value

        # updating the value in accordance
        if attribute == "type":
            symbol.type = value
        elif attribute == "memory_location":
            symbol.memory_location = value
        
        
        return True

    def symbolInTable(self, identifier, scope):
        """
        checks whether a symbol exists in the table in given scope.
        if scope is negative searches in all scopes
        and it only needs to be found in 1 scope
        else false
        returns:
            bool: True if found, False otherwise
        """
        # search all scope
        if scope < 0:
            for symbol_scope in self.symbol_table.values():
                if identifier in symbol_scope:
                    return True
            return False
        # search the given scope
        else:
            return identifier in self.symbol_table.get(scope, {})

    def getSymbol(self, identifier, scope):
        """
        locate and retrieves the SymbolInfo record for the given identifier 
        in the given scope
        returns:
            SymbolInfo or None: The found SymbolInfo record or None if not found
        """
        # if scope is in symbol table and within scope verify the identifier
        if scope in self.symbol_table and identifier in self.symbol_table[scope]:
            return self.symbol_table[scope][identifier]
        return None

    def lookup(self, identifier):
        """
        look for the symbol in the scope stack from the innemost scope(bottom of the stack)
        returns:
            SymbolInfo or None: The SymbolInfo record found, or None if not found
        """
        for scope in reversed(self.scope_stack):
            # look from the inner most scope(local)
            if identifier in self.symbol_table.get(scope, {}):
                return self.symbol_table[scope][identifier]
        return None
