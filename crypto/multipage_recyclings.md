# Multipage recyclings (easy)
This challenge was about exploiting some leak from the encryption process.

Let's see first how the challeng encrypts things:
```python
    def encrypt(self, message):
        iv = os.urandom(16)

        ciphertext = b''
        plaintext = iv

        blocks = self.blockify(message, 16)
        for block in blocks:
            ct = self.cipher.encrypt(plaintext)
            encrypted_block = self.xor(block, ct)
            ciphertext += encrypted_block
            plaintext = encrypted_block

        return ciphertext
```

* For the cipher AES ECB is used.
* A random IV is chosen
* The input is converted into 16 byte blocks
* The IV is encrypted = `ct`
* The plaintext block is xored with `ct` = `encrypted_block`
* `encrypted_block` is used as IV for the next iteration

Now let's see how the leak works:

```python
def leak(self, blocks):
    r = random.randint(0, len(blocks) - 2)
    leak = [self.cipher.encrypt(blocks[i]).hex() for i in [r, r + 1]]
    return r, leak
```

Okay leak chooses 2 random consecutive blocks, encryptes them, and return the indices and the encrypted result.

Finally let's look at how main uses these 2 functions:

```python
    aes = CAES()
    message = pad(FLAG * 4, 16)

    ciphertext = aes.encrypt(message)
    ciphertext_blocks = aes.blockify(ciphertext, 16)

    r, leak = aes.leak(ciphertext_blocks)
```

* The message will be the flag repeated 4 times.
* We encrypt the message
* We leak from the encrypted message

From the output we know that blocks 3 and 4 were leaked.
Now how can we exploit this?

We know how a certain encrypted block is generated
`E = encrypt(P) ^ C`, where
* `E` is the new encrypted block
* `P` is the IV for the current iteration
* `C` is the current plaintext block

But we know that `E` will become `P` in the next iteration:
`F = encrypt(E) ^ D`, where
* `F` is the new encrypted block
* `E` is the encrypted block from the previous equation
* `D` is the current plaintext block

So for the second equation it is the case that we know:
* `F` - because this is in the cipher text
* `encrypt(E)` - because this is a block that was leaked

So `D = F ^ encrypt(E)`.

We can recover 2 plaintext blocks, by xoring an encrypted, leaked block with the cipher text block that has index one higher.

Here is my script to solve the challenge:
```
ct = 'bc9bc77a809b7f618522d36ef7765e1cad359eef39f0eaa5dc5d85f3ab249e788c9bc36e11d72eee281d1a645027bd96a363c0e24efc6b5caa552b2df4979a5ad41e405576d415a5272ba730e27c593eb2c725031a52b7aa92df4c4e26f116c631630b5d23f11775804a688e5e4d5624'
r = 3
phrases = ['8b6973611d8b62941043f85cd1483244', 'cf8f71416111f1e8cdee791151c222ad']

def blockify(message, size):
    return [message[i:i + size] for i in range(0, len(message), size)]

def xor(a, b):
    return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

ct = bytes.fromhex(ct)
blocks = blockify(ct, 16)
print(xor(blocks[4], bytes.fromhex(phrases[0])))
print(xor(blocks[5], bytes.fromhex(phrases[1])))

# HTB{CFB_15_w34k_w17h_l34kz}
```
