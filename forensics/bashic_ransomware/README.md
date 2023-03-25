# Bashic ransomware (hard)
As part of the challenge we get
* Memory dump of the target
* symbols for the target (useful for analyzing memory dump with volatility)
* Encrypted flag file
* traffic capture

First I have looked at the traffic capture file and it was pretty short.
Just one HTTP request/response.
I have extracted the response and placed it in the `stage1.sh` file

Since this is just a bash script we can replace all the `eval` calls with the `echo` command and see what the decoded script looks like.
I have modified `stage1.sh` to print what it would do instead of actually executing it to get the next stage.

It seems that the output is a command which reverses a string and then base64 decodes it. Then the result of this is stored in `$x` and evaluated directly

The next stage I saved in `stage2.sh`

We see that this file imports a gpg key and the encrypts all files with certain extensions.
The encryption works as follows:
* Import hard coded GPG key
* Generate a random key with `/dev/urandom`
* Encrypt this random key using the GPG key from step 1
* Send the encrypted key to the remote
* Use the random key as a key for symmetric AES256 encryption on the specified files
* Remove plaintext files

At this point it must be that the key is somewhere in the memory dump.
Sicne the new files have the `.a59ap` extension, and the random key is used in the same command where the new file is generated I thought it would be a good idea to look for this extension in the memory dump and see if a string matching the key could be around.

And sure enough after doing a simple search for the extension I find it at offset `0x21FFB30` and at offset `0x21FFB71` there is a string which is likely the flag:
* It is 16 characters long
* It contains only alphanumeric characters
* `wJ5kENwyu8amx2RM`

Using the following command I have managed to recover the flag:
```bash
echo "wJ5kENwyu8amx2RM" | gpg --batch -o plain.txt --passphrase-fd 0 --decrypt --cipher-algo AES256 flag.txt.a59ap
```
