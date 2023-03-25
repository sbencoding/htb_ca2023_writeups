# Gunhead (very easy)
Simple command injection vulnerability.

Upon loading the website I checked all the different buttons, and the most interesting was the `command` button on the left.

The `clear` and `storage` command do not seem to communicate with the server, however the `ping` command does.

Our input is being directly passed to `shell_exec`, so we could use a command like:

```
/PING 192.168.10.1; CAT /FLAG.TXT
```

To get the flag.
