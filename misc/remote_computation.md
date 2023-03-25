# Remote computation (easy)
In this challenge we will need to perform some computation coming from a remote

First let's read through the **help** menu

```
Results
---
All results are rounded
to 2 digits after the point.
ex. 9.5752 -> 9.58

Error Codes
---
* Divide by 0:
This may be alien technology,
but dividing by zero is still an error!
Expected response: DIV0_ERR

* Syntax Error
Invalid expressions due syntax errors.
ex. 3 +* 4 = ?
Expected response: SYNTAX_ERR

* Memory Error
The remote machine is blazingly fast,
but its architecture cannot represent any result
outside the range -1337.00 <= RESULT <= 1337.00
Expected response: MEM_ERR
```

So now we know something about rounding and the types of errors we should have.

I will shamelessly pass all the input to `eval` in python.
It would have been funny if they sent an RCE :)

The errors are pretty much already covered by python and the calculation logic is obviously implemented.

```python
from pwn import *
p = remote('165.227.224.40', 30418)

p.sendlineafter(b'>', b'1')

for i in range(0, 500):
    req = p.recvuntil(b'=')
    eq = req.split(b': ')[1][:-2]
    print(eq)
    ans = None
    try:
        ans = round(eval(eq), 2)
        if ans < -1337.00 or ans > 1337.00: ans = 'MEM_ERR'
        else: ans = str(ans)
    except ZeroDivisionError:
        ans = 'DIV0_ERR'
    except SyntaxError:
        ans = 'SYNTAX_ERR'

    print(f' -- {ans}')
    p.sendlineafter(b'>', bytes(ans, 'utf-8'))
p.interactive()
```
