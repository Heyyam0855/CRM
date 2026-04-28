; main.asm - sadə x86 (32-bit, NASM) nümunəsi
; Build:
;   nasm -f elf32 main.asm -o main.o
;   ld -m elf_i386 main.o -o main
; Run:
;   ./main

section .data
    msg db "Salam, x86!", 10
    len equ $ - msg

section .text
    global _start

_start:
    ; Binary 0110 = decimal 6
    mov al, 0b0110

    ; write(1, msg, len)
    mov eax, 4
    mov ebx, 1
    mov ecx, msg
    mov edx, len
    int 0x80

    ; exit(0)
    mov eax, 1
    xor ebx, ebx
    int 0x80
