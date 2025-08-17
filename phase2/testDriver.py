# Test Driver
from stm import SymbolTableManager

def test_symbol_table_manager():
    stm = SymbolTableManager()
    # 1. Initialize your symbol table manager
    stm.initSymTab()
    print("Initialized symbol table with global scope.")
    
    # 2. Add 3 symbols (‘temperature’, ‘velocity’, and ‘temp’) with addSymbol() in global.
    # def addSymbol(self, identifier, symbol_type=None, memory_location=None):
    stm.addSymbol("temperature") 
    stm.addSymbol("velocity")    
    stm.addSymbol("temp")        
    
    # 3. Add the attribute ‘type’ with a value of ‘int’ to temperature and velocity.
    # def addAttributeToSymbol(self, identifier, scope, attribute, value):
    stm.addAttributeToSymbol("temperature", 0, "type", "int")
    stm.addAttributeToSymbol("velocity", 0, "type", "int")
    
    # 4. enter a new scope and record the new scope id (local)
    new_scope = stm.enterScope()
    print(f"Entered new scope: {new_scope}") # expected: 1
    
    # 5. Add 2 more symbols (‘velocity’ and ‘position’) in the local (1)
    stm.addSymbol("velocity")
    stm.addSymbol("position")
    
    # 6. Add the attribute ‘type’ with a value of ‘float’ to velocity. 
    stm.addAttributeToSymbol("velocity", new_scope, "type", "float") # 1  

    # 7. Add attribute ‘type’ with a value ‘int’ to position. 
    stm.addAttributeToSymbol("position", new_scope, "type", "int")   # 1
    
    # 8. Test if ‘temperature’ is in the symbol table with symbolInTable() 
    found_temp = stm.symbolInTable("temperature", -1) # search all scope
    print("8.'temperature' in global scope:", found_temp) # should be in global
    
    # 9. Test if ‘bang’ is in the symbol table with symbolInTable() 
    bang1 = stm.symbolInTable("bang", -1) # search all scope
    print("9.'bang' found in any scope:" ,bang1)
    
    # 10. Retrieve the symbol ‘position’. Retrieve it’s type and print it. 
    position_symbol = stm.getSymbol("position", new_scope)
    if position_symbol:
        print("10.'position' type in local scope: ",position_symbol.attributes.get('type')) 
        # should print int
    
    # 11. Find the symbol ‘velocity’ using lookup(). local velocity with type float
    velocityLkUp = stm.lookup("velocity")
    if velocityLkUp:
        print("11. Local 'velocity' type: " ,velocityLkUp.attributes.get('type'))
        #  should return the local velocity symbol which has type ‘float’. 

    # 12. Use exitScope() to return to the global scope. 
    stm.exitScope()
    print("12. Exited scope. Current scope: ",stm.current_scope) # shold be 0
    
    # 13. Add attributes to the three symbols with addAttributeToSymbol(): 
    stm.addAttributeToSymbol("temperature", 0, "memory_location", "0x800000")
    stm.addAttributeToSymbol("velocity", 0, "memory_location", "0x800020")
    stm.addAttributeToSymbol("temp", 0, "dimensions", 2)
    stm.addAttributeToSymbol("temp", 0, "dimension_bounds", [15, 10])
    stm.addAttributeToSymbol("temp", 0, "memory_location", "0x800040")
    
    # temp value printout
    temp = stm.getSymbol("temp",0)
    print("temp: ", temp)

    # 14. Look up ‘temperature’ with getSymbol() 
    temperature_addAttr = stm.getSymbol("temperature", 0)
    if temperature_addAttr:
        print("14.'temperature':", temperature_addAttr) # should print a list of attr

    # 15. Look up ‘velocity’ with lookup() in the scope you created 
    velocity = stm.getSymbol("velocity", 0) # global
    if velocity:
        print("15. Global 'velocity':", velocity)
    
    # 16. Look up ‘position’ in the symbol table in the scope created earlier. (should be in local)
    local_position = stm.getSymbol("position", new_scope)
    print("16.")
    if local_position:
        print("Symbol 'position' still in scope", new_scope, ":", local_position)
    else:
        print("Symbol 'position' not found in scope", new_scope)

    # 17. Look up ‘velocity’ in the global scope with getSymbol() and then print the attr
    global_velocity = stm.getSymbol("velocity", 0) # global
    if global_velocity:
        print("17. looking 'velocity' in global scope:", global_velocity) # should be 

    # Lookup for an identifier that wasn't added
    bang2 = stm.getSymbol("bang", 0)
    print("18. Lookup for 'bang' returned: ",bang2) # should be None

if __name__ == '__main__':
    test_symbol_table_manager()