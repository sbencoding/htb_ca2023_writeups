# She shells C chells (very easy)
I started by loading the binary into ghidra.

The binary mimics a shell and we can use the *help* command to list all valid commands.

I was obviously interested in the *getflag* command, however there was a password requirement.

This command is handled in the `func_flag` function in ghidra.

```c
  fgets((char *)&local_118,0x100,stdin);
  for (local_c = 0; local_c < 0x4d; local_c = local_c + 1) {
    *(byte *)((long)&local_118 + (long)(int)local_c) =
         *(byte *)((long)&local_118 + (long)(int)local_c) ^ m1[(int)local_c];
  }
  local_14 = memcmp(&local_118,t,0x4d);
  if (local_14 == 0) {
    for (local_10 = 0; local_10 < 0x4d; local_10 = local_10 + 1) {
      *(byte *)((long)&local_118 + (long)(int)local_10) =
           *(byte *)((long)&local_118 + (long)(int)local_10) ^ m2[(int)local_10];
    }
    printf("Flag: %s\n",&local_118);
    uVar1 = 0;
  }
```

So first our input is xored with bytes in `m1`, then we check if the result is same as bytes `t`
Then the flag is retrieved by xoring the result with `m2`.

However since `t` is the result, we can get the flag by xoring `t` with `m2`, both are present in the binary.

```python
t = b'\x2c\x4a\xb7\x99\xa3\xe5\x70\x78\x93\x6e\x97\xd9\x47\x6d\x38\xbd\xff\xbb\x85\x99\x6f\xe1\x4a\xab\x74\xc3\x7b\xa8\xb2\x9f\xd7\xec\xeb\xcd\x63\xb2\x39\x23\xe1\x84\x92\x96\x09\xc6\x99\xf2\x58\xfa\xcb\x6f\x6f\x5e\x1f\xbe\x2b\x13\x8e\xa5\xa9\x99\x93\xab\x8f\x70\x1c\xc0\xc4\x3e\xa6\xfe\x93\x35\x90\xc3\xc9\x10\xe9'

m2 = b'\x64\x1e\xf5\xe2\xc0\x97\x44\x1b\xf8\x5f\xf9\xbe\x18\x5d\x48\x8e\x91\xe4\xf6\xf1\x5c\x8d\x26\x9e\x2b\xa1\x02\xf7\xc6\xf7\xe4\xb3\x98\xfe\x57\xed\x4a\x4b\xd1\xf6\xa1\xeb\x09\xc6\x99\xf2\x58\xfa\xcb\x6f\x6f\x5e\x1f\xbe\x2b\x13\x8e\xa5\xa9\x99\x93\xab\x8f\x70\x1c\xc0\xc4\x3e\xa6\xfe\x93\x35\x90\xc3\xc9\x10\xe9'

l = []
for x in range(0, 0x4d):
    l.append(chr(t[x] ^ m2[x]))

print(''.join(l))
```
