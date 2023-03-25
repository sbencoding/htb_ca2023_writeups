from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
# ${a`Es}."KE`Y`sIZE" = 128
# ${K`EY} = [byte[]] (0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0)
# ${iv} = [byte[]] (0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1)

key = bytearray([0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0])
iv = bytearray([0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1])
content = open('./94974f08-5853-41ab-938a-ae1bd86d8e51.dat', 'rb').read()
print(content[:10])

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
clean = unpad(cipher.decrypt(content), 16)

open('stage2.bin', 'wb').write(clean)
