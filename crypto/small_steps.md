# Small steps (very easy)
In this challenge textbook RSA will be exploited.

```python
    def __init__(self):
        self.q = getPrime(256)
        self.p = getPrime(256)
        self.n = self.q * self.p
        self.e = 3

    def encrypt(self, plaintext):
        plaintext = bytes_to_long(plaintext)
        return pow(plaintext, self.e, self.n)
```

This is the RSA encrypt, implementation the challenge uses.

We get the encrypted value, `n` and `e` from the remote.

The vulnerability here is that `e` is too small, 3 in this case.
When `e` is too small `M^e mod n` becomes `M^e` since it will never go above `n` for certain messages.

This means that we can just take the third root of the encrypted message and get back the flag.

Adapting the solver script with my solution in the `pwn` function

```python
# This script is not necessary for the challenge but may be useful in the
# future.
from pwn import *
import gmpy2
from Crypto.Util.number import long_to_bytes

# This function takes in binary data and converts it to ASCII.
def toAscii(data):
    return data.decode().strip()


# This function sends the string "E" to the server and retrieves the public key
# and encrypted flag that are returned. The public key consists of two parts:
# N and e.
def choiceE():
    r.sendlineafter(b"> ", b"E")
    r.recvuntil(b"N: ")
    N = eval(toAscii(r.recvline()))
    r.recvuntil(b"e: ")
    e = eval(toAscii(r.recvline()))
    r.recvuntil(b"The encrypted flag is: ")
    encrypted_flag = eval(toAscii(r.recvline()))
    return N, e, encrypted_flag


# This function serves as the main logic of the solver script. It calls
# `choiceE()` to retrieve the public key and encrypted flag and prints them.
def pwn():
    N, e, encrypted_flag = choiceE()
    print(N, e, encrypted_flag)
    pt = gmpy2.iroot(encrypted_flag, e)
    print(long_to_bytes(pt[0]))

# This block handles the command-line flags when running `solver.py`. If the
# `REMOTE` flag is set, the script connects to the remote host specified by the
# `HOST` flag. Otherwise, it starts the server locally using `process()`.
if __name__ == "__main__":
    if args.REMOTE:
        ip, port = args.HOST.split(":")
        r = remote(ip, int(port))
    else:
        r = process(["python3", "server.py"])

    pwn()
```
