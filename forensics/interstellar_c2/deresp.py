from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import gzip

key = base64.b64decode('nUbFDDJadpsuGML4Jxsq58nILvjoNu76u4FIHVGIKSQ=')
content = open('resp5.enc', 'rb').read()[1500:]
print(content)
iv = content[:16]
content = content[16:]

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
clean = cipher.decrypt(content)#.replace(b'\x00', b'')
uc = gzip.decompress(clean)

# HTB{h0w_c4N_y0U_s3e_p05H_c0mM4nd?}
open('response5.png', 'wb').write(base64.b64decode(uc))
