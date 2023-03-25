# Janken (easy)
For this challenge we get a binary that will be running on the remote.

First I check the rules of the game, and it seems like a rock, paper, scissors game.
When playing we can type rock, paper, scissors, the opponent will guess as well and we need to win 100 times.
Let's see how the game is implemented in ghidra

```c
  for (; rounds < 100; rounds = rounds + 1) {
    fprintf(stdout,"\n[*] Round [%d]:\n",rounds);
    game();
  }
```

In main we see that the `game` function is called 100 times, let's see what the `game` function does.

```c
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  iVar1 = rand();
  local_78[0] = "rock";
  local_78[1] = "scissors";
  local_78[2] = "paper";
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  local_58[0] = "paper";
  local_58[1] = "rock";
  local_58[2] = "scissors";
  fwrite(&DAT_00102540,1,0x33,stdout);
  read(0,&local_38,0x1f);
  fprintf(stdout,"\n[!] Guru\'s choice: %s%s%s\n[!] Your  choice: %s%s%s",&DAT_00102083,
          local_78[iVar1 % 3],&DAT_00102008,&DAT_0010207b,&local_38,&DAT_00102008);
  local_88 = 0;
  do {
    sVar4 = strlen((char *)&local_38);
    if (sVar4 <= local_88) {
LAB_001017a2:
      pcVar5 = strstr((char *)&local_38,local_58[iVar1 % 3]);
      if (pcVar5 == (char *)0x0) {
        fprintf(stdout,"%s\n[-] You lost the game..\n\n",&DAT_00102083);
                    /* WARNING: Subroutine does not return */
        exit(0x16);
      }
      fprintf(stdout,"\n%s[+] You won this round! Congrats!\n%s",&DAT_0010207b,&DAT_00102008);
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    ppuVar3 = __ctype_b_loc();
    if (((*ppuVar3)[*(char *)((long)&local_38 + local_88)] & 0x2000) != 0) {
      *(undefined *)((long)&local_38 + local_88) = 0;
      goto LAB_001017a2;
    }
    local_88 = local_88 + 1;
  } while( true );
```

First our input is read, and the opponent chooses a random move.
`local_78` is the array of moves for the opponent.
At matching indices `local_58` contains the winning moves that we need to make, important to note how a draw counts as a lose for some reason.

But look at what function is used! `strstr` looks for the second argument in the first argument, and returns the index of the first occurrence or NULL if not found.

Now notice how when reading user input 0x1f bytes are read.

We can just send `rockpaperscissors` on each choice and it would surely contain the winning move!

```python
from pwn import *
p = remote('165.227.224.40', 30509)

payload = 'rockpaperscissors'
p.sendlineafter(b'>>', b'1')

for i in range(99):
    p.sendlineafter(b'>>', b'rockpaperscissors')
    print(f'sent {i}')
p.interactive()
```

For some reason there was an issue with sending this 100 times, so I decreased the count to 99

After this the opponent gives us the flag.
