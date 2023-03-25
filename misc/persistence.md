# Persistence (very easy)
This challenge asks us to send around 1000 request to a `/flag` endpoint.

```python
import requests
for i in range(0, 2000):
    resp = requests.get('http://165.232.108.36:30519/flag')
    if b'HTB' in resp.content: print(resp.content)
```
