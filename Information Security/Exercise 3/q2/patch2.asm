jmp 0x95
lea ecx, [ebp-1036]
mov dl, byte ptr [ecx]
cmp dl, 0x23
jnz 0x6B
mov dl, byte ptr [ecx+1]
cmp dl, 0x21
jnz 0x6B
add ecx, 2
push ecx
call -0x16D
jmp 0x81
