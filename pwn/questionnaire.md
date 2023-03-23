# Questionnaire (very easy)
This challange involves analyzing a binary file, before diving in to exploitation and answering some questions the docker poses.

For the first couple of questions we can get all the information we need from the `file` command

```shell
➜  questionnaire file test
test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5a83587fbda6ad7b1aeee2d59f027a882bf2a429, for GNU/Linux 3.2.0, not stripped
```

> Is this a '32-bit' or '64-bit' ELF? (e.g. 1337-bit)

64-bit

> What's the linking of the binary? (e.g. static, dynamic)


dynamic

> Is the binary 'stripped' or 'not stripped'?

not stripped

For the next command the `pwntools` package is useful (available in `community/python-pwntools` for archlinux).

The `pwn` command can tell us about the various protections the binary has.

```shell
➜  questionnaire pwn checksec test
[*] '/home/ghost/ctf/htb_cyberapocalypse_2022/pwn/questionnaire/test'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

> Which protections are enabled (Canary, NX, PIE, Fortify)?

NX

For the next question we will require some basic reverse engineering. Using any tool here like ghidra, IDA, binaryninja is a valid solution. However we can attempt to use `objdump` for this challenge.

```shell
➜  questionnaire objdump -d test

test:     file format elf64-x86-64

...

00000000004011fa <main>:
  4011fa:       f3 0f 1e fa             endbr64
  4011fe:       55                      push   %rbp
  4011ff:       48 89 e5                mov    %rsp,%rbp
  401202:       b8 00 00 00 00          mov    $0x0,%eax
  401207:       e8 84 ff ff ff          call   401190 <vuln>
  40120c:       90                      nop
  40120d:       5d                      pop    %rbp
  40120e:       c3                      ret

```

> What is the name of the custom function that gets called inside `main()`? (e.g. vulnerable_function())

vuln

For the next question still using `objdump` we find the size of the buffer. Exactly the amount of bytes that the stack pointer gets subtracted by at after the initialization of the stack frame.

```
0000000000401190 <vuln>:
  401190:       f3 0f 1e fa             endbr64
  401194:       55                      push   %rbp
  401195:       48 89 e5                mov    %rsp,%rbp
  401198:       48 83 ec 20             sub    $0x20,%rsp
```

> What is the size of the 'buffer' (in hex or decimal)?

0x20

Sticking with the `objdump` output and inspecting the different function we can discover a function that is never called.

> Which custom function is never called? (e.g. vuln())

gg

Now some exploitation questions are asked:

> What is the name of the standard function that could trigger a Buffer Overflow? (e.g. fprintf())

fgets

> After how many bytes a Segmentation Fault occurs (in hex or decimal)?

40

> What is the address of 'gg()' in hex? (e.g. 0x401337)

0x401176

After this prompt we get the flag!
