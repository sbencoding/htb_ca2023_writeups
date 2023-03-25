# Ancient encodings (very easy)
This challenge just base64 encodes the input, converts it to bytes and writes the hex representation.

To solve this we just do the inverse operation on all of these in reverse order.

```python
import base64
content = open('./output.txt', 'r').read()
cont = bytes.fromhex(content[2:])
print(base64.b64decode(cont).decode('utf-8'))
```
