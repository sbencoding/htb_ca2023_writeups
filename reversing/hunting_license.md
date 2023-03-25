# Hunting license (easy)
First the binary asks us if we are up for the challenge, and we need to reply with `y`

Then the first password is asked, let's see how to get it:
In ghidra we look into the `exam` function and find

```c
  local_10 = (char *)readline(
                             "Okay, first, a warmup - what\'s the first password? This one\'s not ev en hidden: "
                             );
  iVar1 = strcmp(local_10,"PasswordNumeroUno");
```

Okay, so we know that the first password is *PasswordNumeroUno*

Then for the second password we have the following fragment:

```c
  reverse(&local_1c,t,0xb);
  local_10 = (char *)readline("Getting harder - what\'s the second password? ");
  iVar1 = strcmp(local_10,(char *)&local_1c);
```

First `t` is reversed, then it is checked against the user input.

Therefore we take `t` convert it to ASCII and revers it to get *P4ssw0rdTw0*

For the third password the following code is executed:
```c
  xor(&local_38,t2,0x11,0x13);
  local_10 = (char *)readline("Your final test - give me the third, and most protected, password: ")
  ;
  iVar1 = strcmp(local_10,(char *)&local_38);
```

Here we see that the `xor` function is called on `t2` and then the result will need to be equal to our password.

```c
void xor(long param_1,long param_2,ulong length,byte param_4)

{
  int local_c;
  
  for (local_c = 0; (ulong)(long)local_c < length; local_c = local_c + 1) {
    *(byte *)(param_1 + local_c) = *(byte *)(param_2 + local_c) ^ param_4;
  }
  return;
}
```

An this is the xor function, so we see that `local_38` is the destination and `t2` is the input.

The first `0x11` bytes are going to be xored with `0x13`.

After performing the above operations on `t2` we get *ThirdAndFinal!!!*

Now the actual solution to the challenge is answering some interactive question on a docker instance, so let's do that:

> What is the file format of the executable?
elf

> What is the CPU architecture of the executable?
x86_64

> What library is used to read lines for user answers? (`ldd` may help)
readline

> What is the address of the `main` function?
0x401172

> How many calls to `puts` are there in `main`? (using a decompiler may help)
5

> What is the first password?
PasswordNumeroUno

> What is the reversed form of the second password?
0wTdr0wss4P

> What is the real second password?
P4ssw0rdTw0

> What is the XOR key used to encode the third password?
0x13

> What is the third password?
ThirdAndFinal!!!

> [+] Here is the flag: `HTB{l1c3ns3_4cquir3d-hunt1ng_t1m3!}`
