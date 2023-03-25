from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

key = base64.b64decode('DGCzi057IDmHvgTVE2gm60w8quqfpMD+o8qCBGpYItc=')
content = base64.b64decode(open('./first_command', 'r').read())
iv = content[:16]
content = content[16:]

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
clean = base64.b64decode(cipher.decrypt(content).replace(b'\x00', b''))
print(clean.decode("utf-8"))
