# Pandora's box (easy)
For this challenge a simple buffer overflow vulnerability needs to be exploited.

Running the usual `checksec` analysis to see what protections the binary has:
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./glibc/
```

Good! No ASLR for the binary and also no stack canary.

Next I loaded the binary in to Ghidra to see what was happening under the hood.
The interesting function here will be `box()` which is called from `main()` after some setup and the banner.

```c
void box(void)

{
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  long local_10;
  
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  fwrite("This is one of Pandora\'s mythical boxes!\n\nWill you open it or Return it to the Library  for analysis?\n\n1. Open.\n2. Return.\n\n>> "
         ,1,0x7e,stdout);
  local_10 = read_num();
  if (local_10 != 2) {
    fprintf(stdout,"%s\nWHAT HAVE YOU DONE?! WE ARE DOOMED!\n\n",&DAT_004021c7);
                    /* WARNING: Subroutine does not return */
    exit(0x520);
  }
  fwrite("\nInsert location of the library: ",1,0x21,stdout);
  fgets((char *)&local_38,0x100,stdin);
  fwrite("\nWe will deliver the mythical box to the Library for analysis, thank you!\n\n",1,0x4b,
         stdout);
  return;
}
```

If we input anything other than 2, then we fail the challenge, so let's input 2.

Next up `fgets` is called, and the buffer overflow happens here.
As we see from the variables on the top, the current stack frame is only 40 bytes, however 0x100 (256) bytes are being read.

Unlike the previous challenge here we don't have a *win function* therefore we will aim for arbitrary code execution, i.e get a shell.

I chose to solve this challenge using the `ret2libc` technique, so in order to find out where the libc functions are loaded I needed to leak the libc address.

Thankfully remember that the binary itself doesn't have ASLR therefore we know where the PLT and the GOT are.
Using this information we can construct our first exploit that will leak the libc address of the puts function.

```
[40 - padding] + [8 - old RBP] + [8 - ret gadget] + [8 - pop rdi; ret gadget] + [8 - puts@got] + [8 - puts@plt] + [8 - box function address]
```

The first gadget will just pop the next location to execute from the stack and jump to it. We need this to fix stack pointer alignment to 16 bytes, which some functions are sensitive to.

The next gadget will pop from the stack into RDI and then return. Essentially this allows us to call single argument functions. The address in the GOT where puts is will be the argument and the `puts` function will be the function we call.

This will essentially call `puts(puts)`, resulting in the address of the puts function being leaked.

We finish up with the address of `box` since after the leak we want to continue our exploit to get the shell.

Now that we know the address of puts, we can figure out where libc is being loaded.
Then we can look for the `system` function in libc and the `/bin/sh` string.

Once we have these a second stage payload is constructed
```
[40 - padding] + [8 - old RBP] + [8 - ret gadget] + [8 - pop rdi; ret gadget] + [8 - /bin/sh string address] + [8 - system]
```

Here again we first align the stack, and then call `system("/bin/sh")` to get our shell.

Once the exploit goes through we can just print the flag from our shell.
