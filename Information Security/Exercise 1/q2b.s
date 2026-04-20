# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # <<<< PUT YOUR CODE HERE >>>>
    MOV ECX, DWORD PTR [ESP + 4]
    
    # edge cases
    CMP ECX, 1
    JL _condition0
    JE _condition1
    
    #init values
    MOV EBX, 0 # a=0
    MOV EDX, 1 # b=1
    DEC ECX # offset loop counter
    
    _loop:
        # compute a^2
        IMUL EBX, EBX
        
        # next = a^2
        MOV EAX, EBX
        
        # compute b^2
        MOV EBX, EDX
        IMUL EBX, EBX
        
        # next = next + b^2 = a^2 + b^2
        ADD EAX, EBX
        
        # a,b = b,next
        MOV EBX, EDX
        MOV EDX, EAX
        
        DEC ECX
        CMP ECX, 0
        JNE _loop
        JE _return 
    
    
    _condition0:
        MOV EAX, 0
        JMP _return
    _condition1:
        MOV EAX, 1
        
    _return:
        RET
