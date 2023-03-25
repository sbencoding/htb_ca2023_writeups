from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

content = open('./stage2.enc', 'r').read()
content = base64.b64decode(content)

key = bytes.fromhex('99b97bf329968477cc3aae5dd24fdc12a04177b98f66444e03a9a14c2b1758823a85861eccaadc8ecd4f 36d201a510ce')[:32]
iv = bytes.fromhex('3a85861eccaadc8ecd4f36d201a510ce')

print(len(key), key)
print(len(iv), iv)

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
clean = unpad(cipher.decrypt(content), 16)
open('stage2.bin', 'wb').write(clean)
