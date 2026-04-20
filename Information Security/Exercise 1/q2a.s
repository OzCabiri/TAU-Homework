# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # <<<< PUT YOUR CODE HERE >>>>
    PUSH EBP
    MOV EBP, ESP
    
    MOV EBX, DWORD PTR [ESP + 8] # get input which is above old EBP and RA
    
    CMP EBX, 1
    JL _condition0
    JE _condition1
    
    #call function on n-1
        DEC EBX #n-1
        PUSH EBX
        CALL my_function
    
    IMUL EAX, EAX #a_(n-1)^2
    PUSH EAX #save on stack
    MOV EBX, DWORD PTR [ESP+4] #get n-1
    
    #call function on n-2
        DEC EBX
        PUSH EBX
        CALL my_function
    
    IMUL EAX, EAX #a_(n-2)^2
    MOV EBX, DWORD PTR [ESP+4] #get a_(n-1)^2
    ADD EAX, EBX
    JMP _finalize
    
    
    _condition0:
        MOV EAX, 0
        JMP _finalize
        
    _condition1:
        MOV EAX, 1
        
    _finalize:
        MOV ESP, EBP
        POP EBP
        RET
    
    # 2. Save the result in the register EAX (and then return!).
    # 3. Make sure to include a recursive function call (the recursive function
    #    can be this function, or a helper function defined later in this file).
