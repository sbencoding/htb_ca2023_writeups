# Restricted (easy)
In this challenge we will try to bypass a restricted bash shell

From the `Dockerfile` we see that a restricted environment is set up.
* Our user will be the **restricted** user
* As shell we will have `rbash`
* We will have access to 3 executables: `top`, `uptime` and `ssh`
* Our path is restricted to the `.bin` folder in our home directory

Reading the ssh configuration I found the following line:
```
Match user restricted
    PermitEmptyPasswords yes
```

Okay so we can log in using the **restricted** user through ssh.

Once on the system it seems that we can't do anything.
This is a good time to go to [GTFO bins](https://gtfobins.github.io/) to see if there is any way to escape our restricted environment.

`top` and `uptime` don't seem helpful, however `ssh` seems promising.

I went to the file read section, which suggested a way to read files outside of the restricted environment.

From the docker file we already know the flag is in `/flag<random>`, so we use the following command on the remote:

```
ssh -F /flag* localhost -p 1337
```

This will read us the flag :)
