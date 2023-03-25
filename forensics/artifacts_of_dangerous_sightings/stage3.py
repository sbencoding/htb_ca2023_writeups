cont = open('./stage3.ps1', 'r').read().split(' + ')

buf = []
for tok in cont:
    ccode = int(tok[6:])
    buf.append(chr(ccode))

print(''.join(buf))
