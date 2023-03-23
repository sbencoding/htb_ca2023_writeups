# Getting started (very easy)
This challenge focuses on making sure we know how to interact through `pwntools` with binaries and remotes.

`gs` contains a buffer overflow vulnerability and prompts us to overflow the buffer.

As can be seen from the nice output, we need 40 bytes to reach the target and then 8 more byte to overwrite it
```
After we insert 4 "B"s, (the hex representation of B is 0x42), the stack layout looks like this:


      [Addr]       |      [Value]
-------------------+-------------------
0x00007fffdaf5a1b0 | 0x4242424241414141 <- Start of buffer
0x00007fffdaf5a1b8 | 0x0000000000000000
0x00007fffdaf5a1c0 | 0x0000000000000000
0x00007fffdaf5a1c8 | 0x0000000000000000
0x00007fffdaf5a1d0 | 0x6969696969696969 <- Dummy value for alignment
0x00007fffdaf5a1d8 | 0x00000000deadbeef <- Target to change
0x00007fffdaf5a1e0 | 0x000055b091327800 <- Saved rbp
0x00007fffdaf5a1e8 | 0x00007f7f17c21c87 <- Saved return address
0x00007fffdaf5a1f0 | 0x0000002000000000
0x00007fffdaf5a1f8 | 0x00007fffdaf5a2c8
```

After constructing this payload in the provided wrapper script, we can point it at the remote and get the flag
