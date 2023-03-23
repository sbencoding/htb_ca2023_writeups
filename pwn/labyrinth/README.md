# Labyrinth (easy)
This challenge involves exploiting a simple buffer overflow and then redirecting execution to a different function.

First we check the protections the binary has, using `checksec`
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./glibc/'
```

Pretty much nothing, there's no canary and no ASLR.

Loading the binary into Ghidra, I analyzed the `main` function.

```c
undefined8 main(void)

{
  int iVar1;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  char *local_18;
  ulong local_10;
  
  setup();
  banner();
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  fwrite("\nSelect door: \n\n",1,0x10,stdout);
  for (local_10 = 1; local_10 < 0x65; local_10 = local_10 + 1) {
    if (local_10 < 10) {
      fprintf(stdout,"Door: 00%d ",local_10);
    }
    else if (local_10 < 100) {
      fprintf(stdout,"Door: 0%d ",local_10);
    }
    else {
      fprintf(stdout,"Door: %d ",local_10);
    }
    if ((local_10 % 10 == 0) && (local_10 != 0)) {
      putchar(10);
    }
  }
  fwrite(&DAT_0040248f,1,4,stdout);
  local_18 = (char *)malloc(0x10);
  fgets(local_18,5,stdin);
  iVar1 = strncmp(local_18,"69",2);
  if (iVar1 != 0) {
    iVar1 = strncmp(local_18,"069",3);
    if (iVar1 != 0) goto LAB_004015da;
  }
  fwrite("\nYou are heading to open the door but you suddenly see something on the wall:\n\n\"Fly li ke a bird and be free!\"\n\nWould you like to change the door you chose?\n\n>> "
         ,1,0xa0,stdout);
  fgets((char *)&local_38,0x44,stdin);
LAB_004015da:
  fprintf(stdout,"\n%s[-] YOU FAILED TO ESCAPE!\n\n",&DAT_00402541);
  return 0;
}
```

First, 69 should be provided as a door number, in order to get into the vulnerable path of execution.

Then `fgets` will read 0x44 bytes into `local_38`. We see at the top of the function that is has 6 variables on the stack starting from `local_38`, each is 8 bytes large.

Then we can overwrite the RBP of the calling function and then the **return address**.

Browsing the list of functions in Ghidra, I found the `escape_strategy` function, which gives us the flag.

As a final trick, stack alignment was an issue, therefore a ROP gadgets needed to be added to the payload, in order to align the stack pointer to 16 bytes again.
To fix alignment a simple `ret` ROP gadget can be placed. This will just pop the element from the stack and set the program counter to it.

To find the ROP gadget I will use the `pwntools` functions.

So our payload that gets put on the stack will be:
```
[48 - padding] + [8 - RBP overwrite] + [8 - ret gadget] + [8 - win function address]
```

Running `solve.py` will give us the flag.
