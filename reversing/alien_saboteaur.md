# Alien saboteaur (medium)
We get a virutal machine and a binary it can execute.

The binary asks us for the keycode. Which I don't know.

Next I opened up ghidra on the `vm` to see how it works.
Basically it loads the specified binary and allocates some space on the heap that will store the binary itself, the program counter and some additional space.

Then the virtual machine is started with `vm_run`, which keeps executing instructions with `vm_step`.

This function will get the op code from the blob and then use that as an index into the instruction lookup table to perform a certain action.

Especially interesting instructions at this point are: `vm_je` and `vm_jne`
After the flag is read it must be that it is compared to some already existing value

Using gdb I have set a breakpoint on `vm_je` and sure enough I saw that my flag values were getting compared.

The keycode length needs to be 17 as that is when execution goes from reading the input to checking it.

However, before comparison got the the end of my flag, I saw that suddenly -1 and 0 were compared, which was odd, since I had neither values in my flag.

After continuing I saw: *Terminal blocked!*

I put 2 and 2 together and thought immediately that there must be some anti debugging technique at play here.

After looking around more I found the `vm_inv` function makes a syscall, so I loaded the binary with `strace`.
And sure enough after entering the passcode `c0d3_r3d_5hAAAAAA` I saw:
```
ptrace(PTRACE_TRACEME)                  = -1 EPERM (Operation not permitted)
```
So indeed the binary tries to attach a debugger but can't if some other tool is already debugging it.

To get around this problem I simply set a conditional breakpoint on the `vm_je` function for whenever the compared values don't match. When I got to the -1 to 0 comparison again, I just set the values to be equal, and now we are onto the second password.

After experimentation I found out that this password needs to be 36 characters long.

Then similar to the previous password `vm_je` gets invoked, however this time I didn't see my input character anywhere.

After trying an input full of `A`, then `B`, then `C` I have noticed that the value being compared and then one I enter is different, because the entered values get xored by 2.
So now I knew that if I xor the value coming from the binary with 2, that will need to be my input.

The last thing to figure out was that the password was not compared from left to right, but from different positions.
By having an input string with unique characters, I have managed to trakc down which position was being compared to what character.

Finally having replaced all characters I have arrived at the flag:
**HTB{5w1rl_4r0und_7h3_4l13n_l4ngu4g3}**
