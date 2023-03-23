# Void (medium)
This challenge contains a buffer overflow vulnerability again, however this time we don't have many functions to play with in the PLT/GOT.

First let's check the protections of the binary using `checksec`

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./glibc/'
```

We see that nothing except NX is enabled. This is different compared to the previous challenges that had **Full RELRO**, this challenge only has **Partial RELRO**, meaning there's possibly some GOT overwriting we need to do in order to win.

Then I loaded the binary in Ghidra and it was very minimal, essentially calling just the `vuln()` function.

```c
void vuln(void)

{
  undefined local_48 [64];
  
  read(0,local_48,200);
  return;
}
```

Here we see the buffer overflow vulnerability, where `read()` reads 200 bytes which is over the defined size 64.

After the contest I have seen that this is supposed to be solved using the `ret2dlresolve` technique, however at the time of the contest I was unaware of this technique, therefore I have yet again decided to leak libc and aim for an arbitrary code execution exploit.

After trying and failing at this task, I realized that I don't necessarily need to leak the libc base address, it is also enough if I can find a gadget to offset the current `read()` address in the GOT to call something useful.

The idea is as follows:
1. Offset read GOT by some bytes to point to a **one_gadget**
2. Call `vuln()` again which will call `read@plt` that will now point to our one_gadget instead.

A **one_gadget** is a location in libc that will execute a shell for us.
This means that we don't have to actually setup the full ROP chain and find out where the `/bin/sh` strings is.
The small caveat is that some restrictions apply in order to make these gadgets work, which is often some variables or memory locations being 0.

To find one gadgets we can use the `one_gadget` program (from the `community/one_gadget` package in archlinux)

```
➜  void one_gadget glibc/libc.so.6
egrep: warning: egrep is obsolescent; using grep -E
egrep: warning: egrep is obsolescent; using grep -E
egrep: warning: egrep is obsolescent; using grep -E
egrep: warning: egrep is obsolescent; using grep -E
0xc961a execve("/bin/sh", r12, r13)
constraints:
  [r12] == NULL || r12 == NULL
  [r13] == NULL || r13 == NULL

0xc961d execve("/bin/sh", r12, rdx)
constraints:
  [r12] == NULL || r12 == NULL
  [rdx] == NULL || rdx == NULL

0xc9620 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
```

Here we have our gadgets and the constraints, however we still need to figure out how to make this appear in the GOT instead of `read()`

Here I used the `ROPGadget` command (from the `community/ropgadget` in archlinux) to find some gadgets in the binary.

Here I have found many gadgets with the `add` instructions, however not many of them were particularly useful to me, either the written data was uncontrollable or I haven't had control over the register holding the destination.

However a gadget did seem promising if I could control the involved registers:
```
add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret
```

This will perform an addition a nop and then return, perfect for us if we control `rbp` and `ebx`.

Now we only need to control `rbp` and `ebx`, which can be done using `ret2csu`.
Specifically I will jump to the following section:
```
        004011b2 5b              POP        RBX
        004011b3 5d              POP        RBP
        004011b4 41 5c           POP        R12
        004011b6 41 5d           POP        R13
        004011b8 41 5e           POP        R14
        004011ba 41 5f           POP        R15
        004011bc c3              RET
```

This will allow us the set `rbp` and `rbx`, furthermore by zeroing `r12` and `r13` we can make the first gadget returned by `one_gadget` work.

Therefore the process will look like this:
1. Setup `rbp` and `rbx` to target `read@got` and add offset from one_gadget to read
2. Call the `add` gadget
3. Call `vuln()` again

The payload will have the following layout:
```
[8 - CSU gadget address] + [8 - rbx overwrite, the offset] + [8 - pointer to read@got] + [32 - zero out r12-r15] + [8 - address of memory add gadget] + [8 - address of vuln]
```

Running `solve.py` will get us a shell, which we can use to get the flag.
