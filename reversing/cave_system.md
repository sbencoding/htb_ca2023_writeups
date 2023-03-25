# Cave system (easy)
In this challenge a bunch of condition are checked against the user input.
The user input is the flag itself.

```c
  fgets(local_88,0x80,stdin);
  iVar1 = memcmp(local_88,&DAT_00102033,4);
  if (((((((iVar1 == 0) && ((char)(local_88[21] * local_88[48]) == '\x14')) &&
         ((char)(local_88[32] - local_88[36]) == -6)) &&
        (((((((char)(local_88[37] - local_88[26]) == -0x2a &&
             ((char)(local_88[16] - local_88[48]) == '\b')) &&
            (((char)(local_88[55] - local_88[8]) == -0x2b &&
             (((char)(local_88[26] * local_88[7]) == -0x13 &&
              ((char)(local_88[4] * local_88[24]) == -0x38)))))) &&
           ((byte)(local_88[34] ^ local_88[28]) == 0x55)) &&
          (((((char)(local_88[30] - local_88[55]) == '4' &&
             ((char)(local_88[59] + local_88[50]) == -0x71)) &&
            ((char)(local_88[44] + local_88[27]) == -0x2a)) &&
           (((byte)(local_88[17] ^ local_88[14]) == 0x31 &&
            ((char)(local_88[56] * local_88[20]) == -0x54)))))) &&
         (((((char)(local_88[58] - local_88[26]) == -0x3e &&
            (((byte)(local_88[26] ^ local_88[6]) == 0x2f &&
             ((byte)(local_88[14] ^ local_88[39]) == 0x5a)))) &&
           ((byte)(local_88[44] ^ local_88[39]) == 0x40)) &&
          (((((local_88[40] == local_88[26] && ((char)(local_88[23] + local_88[49]) == -0x68)) &&
             ((char)(local_88[23] * local_88[59]) == 'h')) &&
            (((char)(local_88[1] - local_88[28]) == -0x25 &&
             ((char)(local_88[24] - local_88[29]) == -0x2e)))) &&
           (((char)(local_88[38] - local_88[24]) == '.' &&
            (((byte)(local_88[32] ^ local_88[22]) == 0x1a &&
             ((char)(local_88[44] * local_88[4]) == -0x60)))))))))))) &&
       ((((((char)(local_88[38] * local_88[27]) == '^' &&
           ((((char)(local_88[15] - local_88[40]) == -0x38 &&
             ((byte)(local_88[49] ^ local_88[53]) == 0x56)) &&
            ((byte)(local_88[26] ^ local_88[45]) == 0x2b)))) &&
          ((((((byte)(local_88[54] ^ local_88[9]) == 0x19 &&
              ((char)(local_88[28] - local_88[47]) == '\x1a')) &&
             (((char)(local_88[50] + local_88[19]) == -0x5f &&
              (((char)(local_88[37] + local_88[57]) == 'V' &&
               ((byte)(local_88[29] ^ local_88[18]) == 0x38)))))) &&
            ((byte)(local_88[44] ^ local_88[60]) == 9)) &&
           ((((((char)(local_88[15] * local_88[38]) == 'y' &&
               ((byte)(local_88[37] ^ local_88[30]) == 0x5d)) &&
              ((char)(local_88[2] * local_88[32]) == '\\')) &&
             (((char)(local_88[10] * local_88[18]) == '9' && (local_88[29] == local_88[21])))) &&
            (((char)(local_88[35] * local_88[21]) == '/' &&
             (((char)(local_88[8] * local_88[37]) == -0x55 &&
              ((char)(local_88[39] + local_88[26]) == -0x6d)))))))))) &&
         (((((((byte)(local_88[26] ^ local_88[34]) == 0x73 &&
              ((((byte)(local_88[20] ^ local_88[31]) == 0x40 &&
                ((char)(local_88[25] + local_88[16]) == -0x57)) &&
               ((byte)(local_88[39] ^ local_88[59]) == 0x15)))) &&
             ((((char)(local_88[0] + local_88[59]) == 'i' &&
               ((char)(local_88[34] + local_88[46]) == -0x5b)) &&
              (((byte)(local_88[30] ^ local_88[52]) == 0x37 &&
               (((char)(local_88[0] * local_88[28]) == '\b' &&
                ((char)(local_88[34] - local_88[56]) == -0x3b)))))))) &&
            ((char)(local_88[18] + local_88[60]) == -0x1c)) &&
           (((((byte)(local_88[35] ^ local_88[40]) == 0x6e &&
              ((char)(local_88[56] * local_88[16]) == -0x54)) &&
             ((char)(local_88[54] - local_88[47]) == '\r')) &&
            ((((char)(local_88[30] + local_88[55]) == -100 &&
              ((char)(local_88[6] + local_88[33]) == -0x2c)) &&
             (((char)(local_88[7] * local_88[29]) == -0x13 &&
              (((byte)(local_88[56] ^ local_88[29]) == 0x38 &&
               ((char)(local_88[1] * local_88[37]) == 'd')))))))))) &&
          (((byte)(local_88[56] ^ local_88[58]) == 0x46 &&
           (((((((char)(local_88[2] * local_88[19]) == '&' &&
                ((byte)(local_88[26] ^ local_88[22]) == 0x2b)) &&
               ((char)(local_88[1] + local_88[7]) == -0x79)) &&
              (((byte)(local_88[27] ^ local_88[0]) == 0x2a &&
               ((char)(local_88[21] - local_88[1]) == '\v')))) &&
             ((char)(local_88[27] + local_88[54]) == -0x32)) &&
            (((byte)(local_88[17] ^ local_88[13]) == 0x3b &&
             ((char)(local_88[19] - local_88[58]) == '\x12')))))))))) &&
        ((((local_88[17] == local_88[10] &&
           ((((char)(local_88[14] - local_88[58]) == 'M' &&
             ((char)(local_88[42] * local_88[52]) == 'N')) && (local_88[50] == local_88[32])))) &&
          (((byte)(local_88[47] ^ local_88[51]) == 0x38 &&
           ((char)(local_88[38] + local_88[25]) == -0x6c)))) &&
         ((char)(local_88[41] + local_88[52]) == -0x31)))))) &&
      ((((local_88[44] == local_88[20] && ((char)(local_88[12] + local_88[25]) == 'f')) &&
        (((char)(local_88[60] + local_88[36]) == -0xf &&
         ((((char)(local_88[41] - local_88[21]) == '\x11' &&
           ((char)(local_88[36] - local_88[49]) == 'D')) &&
          ((char)(local_88[9] - local_88[35]) == 'D')))))) &&
       ((((byte)(local_88[53] ^ local_88[51]) == 1 && ((byte)(local_88[34] ^ local_88[57]) == 0xd))
        && ((((char)(local_88[11] - local_88[28]) == -0x15 &&
             (((((char)(local_88[23] + local_88[24]) == -0x67 &&
                ((char)(local_88[24] + local_88[13]) == -0x6b)) &&
               (((char)(local_88[12] - local_88[0]) == -0x17 &&
                (((((char)(local_88[34] + local_88[31]) == '`' &&
                   ((char)(local_88[5] + local_88[53]) == -0x6a)) &&
                  ((char)(local_88[49] * local_88[42]) == '`')) &&
                 (((char)(local_88[48] * local_88[21]) == '\x14' &&
                  ((char)(local_88[27] - local_88[52]) == '\x03')))))))) &&
              ((char)(local_88[57] + local_88[20]) == -0x6b)))) &&
            ((((char)(local_88[10] * local_88[53]) == -0x26 &&
              ((char)(local_88[1] + local_88[41]) == -0x3c)) &&
             (((char)(local_88[47] - local_88[1]) == '\v' &&
              (((local_88[43] == local_88[19] && ((char)(local_88[39] + local_88[47]) == -0x6d)) &&
               ((char)(local_88[12] * local_88[58]) == 'Q')))))))))))))) &&
     (((((char)(local_88[8] * local_88[26]) == 'A' && ((char)(local_88[46] - local_88[31]) == 'E'))
       && ((char)(local_88[7] + local_88[37]) == 'h')) &&
      (((((char)(local_88[36] + local_88[4]) == -0x44 &&
         ((char)(local_88[31] + local_88[32]) == -0x5e)) &&
        (((char)(local_88[25] + local_88[5]) == 'e' &&
         ((((char)(local_88[43] * local_88[29]) == -0x13 &&
           ((byte)(local_88[13] ^ local_88[45]) == 0x10)) &&
          ((char)(local_88[48] - local_88[12]) == ';')))))) &&
       (((((char)(local_88[23] - local_88[8]) == '\t' &&
          ((byte)(local_88[7] ^ local_88[42]) == 0x41)) &&
         ((char)(local_88[5] - local_88[43]) == -3)) &&
        (((((byte)(local_88[60] ^ local_88[18]) == 0x1a &&
           ((byte)(local_88[1] ^ local_88[3]) == 0x2f)) &&
          (((char)(local_88[17] - local_88[39]) == '+' &&
           (((((char)(local_88[8] + local_88[20]) == -0x2d &&
              ((char)(local_88[11] * local_88[53]) == -0x28)) &&
             ((char)(local_88[27] + local_88[6]) == -0x2e)) &&
            (((char)(local_88[5] + local_88[3]) == -0x55 &&
             ((char)(local_88[35] - local_88[47]) == -0x2e)))))))) &&
         ((byte)(local_88[16] ^ local_88[33]) == 0x10)))))))))) {
    puts("Freedom at last!");
  }
```

Now I promised myself to get more familiar with `angr` and tools as such before the contest, however I didn't have time. Reversing challenges that are solved with symbolic exeuction/SAT solving are somewhat popular I would say, still I had the pleasure of solving this by hand.

Because this is a flag, we know that the first four characters are `HTB{`.
Then we can look for conditions where we know on side of the check, and try to see if there's a singular solution to the condition e.g `<known value> <some opeartion> <unknown value> == <constant>`.

Turns out there are quite some characters for which this is the case. As we start resolving more and more symbols this becomes easier. And finally get the flag.

HTB{H0p3_u_d1dn't_g3t_th15_by_h4nd,1t5_4_pr3tty_l0ng_fl4g!!!}

And the flag even jokes about my solution to the problem. For my next CTF I'll definitely read up on and practice with the intended method.
