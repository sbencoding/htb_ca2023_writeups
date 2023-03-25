# Artifacts of dangerous sightings (medium)
For this challenge we get a `.vhdx` dump file and the first part of the challenge is opening this file.

Thankfully there's a [gist](https://gist.github.com/allenyllee/0a4c02952bf695470860b27369bbb60d) on how to do this.

Instead of following the mount command specified in the guide, allow me some hindsight and let's mount the container in a way that will be helpful later, I'll explain why.

```shell
➜  HostEvidence_PANDORA sudo modprobe nbd max_part=16
➜  HostEvidence_PANDORA sudo qemu-nbd -c /dev/nbd0 ./2023-03-09T132449_PANDORA.vhdx
➜  HostEvidence_PANDORA sudo partprobe /dev/nbd0
➜  HostEvidence_PANDORA sudo mount -t ntfs -o ro,streams_interface=windows /dev/nbd0p1 ./mnt
```

Now the disk dump file is mounted under the local `mnt` folder, let's explore inside.
For forensics challenges a common file I check if possible is the console history, to see if I can extract any useful information.
We are in luck, it seems that this file exists in this dump.

```
type finpayload > C:\Windows\Tasks\ActiveSyncProvider.dll:hidden.ps1
exit
Get-WinEvent
Get-EventLog -List
wevtutil.exe cl "Windows PowerShell" 
wevtutil.exe cl Microsoft-Windows-PowerShell/Operational
Remove-EventLog -LogName "Windows PowerShell"
Remove-EventLog -LogName Microsoft-Windows-PowerShell/Operational
Remove-EventLog 
```

Okay so first an **alternate data stream** is created in the `ActiveSyncProvider.dll` file and then a bunch of event logs are cleaned out.
Now this is where it makes sense that I replaced the mount command, to use `ntfs-3g` and to provide the `streams_interface=windows` option.
This will allow us to access the alternate data stream.

```shell
➜  HostEvidence_PANDORA cat mnt/C/Windows/Tasks/ActiveSyncProvider.dll:hidden.ps1
```

This command will give use a large powershell command, which I have included in the `hidden.ps1` file.

After decoding the base64 string and removing null bytes, we get the result I have placed in `stage2.ps1`. It looks heavily obfuscated, however at the end we see that a string is passed into execution with `|& ${=@!~!}`

So let's execute the script without the execution part in an online interpreter and see what we can get, the result is placed in `stage3.ps1`.

These are just a bunch of ascii characters concatanated, so I wrote the `stage3.py` script to decode it.
The decoded result is placed in `final.ps1`

And the source code contains the flag
```ps1
$TopSecretCodeToDisableScript = "HTB{Y0U_C4nt_St0p_Th3_Alli4nc3}"
```
