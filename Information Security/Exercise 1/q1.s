# Declare the assembly flavor to use the intel syntax.
.intel_syntax noprefix

# Define a symbol to be exported from this file.
.global my_function

# Declare symbol type to be a function.
.type my_function, @function

# Code follows below.

my_function:
    # This code reads the first argument from the stack into EBX.
    # (If you need, feel free to edit/remove this line).
    MOV EBX, DWORD PTR [ESP + 4]

    # <<<< PUT YOUR CODE HERE >>>>
    MOV EAX, 0
    
    _loop:
        INC EAX
        MOV ECX, EAX
        IMUL ECX, ECX
        CMP ECX, EBX
        JL _loop
        
    JNE _noroot
    RET
    
    _noroot:
        MOV EAX, 0

    # This returns from the function (call this after saving the result in EAX).
    # (If you need, feel free to edit/remove this line).
    RET
