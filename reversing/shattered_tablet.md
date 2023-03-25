# Shattered tablet (very easy)
I loaded the binary into ghidra and saw a bif `if` statement

```c
  printf("Hmmmm... I think the tablet says: ");
  fgets(local_48,0x40,stdin);
  if (((((((((local_48[31] == 'p') && (local_48[1] == 'T')) && (local_48[7] == 'k')) &&
          ((local_48[36] == 'd' && (local_48[11] == '4')))) &&
         ((local_48[20] == 'e' && ((local_48[10] == '_' && (local_48[0] == 'H')))))) &&
        (local_48[34] == 'r')) &&
       ((((local_48[35] == '3' && (local_48[25] == '_')) && (local_48[2] == 'B')) &&
        (((local_48[29] == 'r' && (local_48[3] == '{')) &&
         ((local_48[26] == 'b' && ((local_48[5] == 'r' && (local_48[13] == '4')))))))))) &&
      (((local_48[30] == '3' &&
        (((local_48[19] == 'v' && (local_48[12] == 'p')) && (local_48[33] == '1')))) &&
       (((local_48[27] == '3' && (local_48[17] == 'n')) &&
        (((local_48[4] == 'b' && ((local_48[32] == '4' && (local_48[9] == 'n')))) &&
         (local_48[16] == ',')))))))) &&
     (((((((local_48[8] == '3' && (local_48[6] == '0')) && (local_48[23] == 't')) &&
         ((local_48[15] == 't' && (local_48[24] == '0')))) &&
        ((local_48[14] == 'r' && ((local_48[37] == '}' && (local_48[21] == 'r')))))) &&
       (local_48[22] == '_')) && ((local_48[18] == '3' && (local_48[28] == '_')))))) {
    puts("Yes! That\'s right!");
  }
```

Basically check if we have entered the correct flag.

To get the flag I have copied the conditions into a separate python script and replaced `==` with `=`
