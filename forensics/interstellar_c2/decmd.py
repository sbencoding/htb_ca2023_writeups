from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
# ${a`Es}."KE`Y`sIZE" = 128
# ${K`EY} = [byte[]] (0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0)
# ${iv} = [byte[]] (0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1)

key = base64.b64decode('nUbFDDJadpsuGML4Jxsq58nILvjoNu76u4FIHVGIKSQ=')
content = base64.b64decode(open('cmd3.enc', 'r').read())
iv = content[:16]
content = content[16:]

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
clean = base64.b64decode(cipher.decrypt(content).replace(b'\x00', b''))
parts = clean.decode('utf-8').replace('multicmd', '').split('!d-3dion@LD!-d')
for p in parts:
    tid = p[0:5]
    cmd = p[5:]

    print(f'{tid}: {cmd[:32]}')
