# UnEartly Shop (hard)
In this challenge we will exploit NoSQL inejction and php deserialization to get the flag.

First we are greeted with a list of products, and we can put them on the wishlist (offline) and place and order on them.
Here note that listing the products is a POST request oddly enough instead of a get.

I check the request and I see that some JSON is being passed that looks like a mongodb query.
I check the mongodb [documentation](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith) to find out what options we have and I find the `unionWith` option.

Now checking the `entrypoint.sh` file we know what collections there are, so we can simply send the following request to the products endpoint:
```json
[
	{
		"$unionWith": "users"
	}
]
```

The response will contain the username and password of all users, which is only the admin in our case.
In the response I also spotted the `access` field, which seems to be a PHP serialized array.

Now we can login with the admin users and see what it can do.
Most of the functionality seems fake, however we can use the edit user feature, to change the password of a user.

Now let's take a look at what happens when the user password is upadted:
```json
{
	"_id": 1,
	"password": "password",
	"username": "admin"
}
```

Let's try and see if we can somehow abuse this request again to our advantage.

```php
// backend/controllers/UserController.php
    public function update($router)
    {
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);

        if (!$data['_id'] || !$data['username'] || !$data['password'])
        {
            $router->jsonify(['message' => 'Insufficient parameters!'], 400);
        }

        if ($this->user->updateUser($data)) {
            $router->jsonify(['message' => 'User updated successfully!']);
        }

        $router->jsonify(['message' => 'Something went wrong!', 'status' => 'danger'], 500);
    }
```

Here we see that it verifies that the `id`, `username` and `password` fields are in the request and then updates the user data.

```php
// backend/models/UserModel.php
    public function updateUser($data)
    {
        return $this->database->update('users', $data['_id'], $data);
    }
```

Here is the code that triggers the database update, we see it just passes the collection name the idea and **all data**

```php
// backend/Database.php
    public function update($collection, $index, $data)
    {
        $collection = $this->db->$collection;

        $updateResult = $collection->updateOne(
            [ '_id' => intval($index) ],
            [ '$set' => $data ]
        );

        if ($updateResult->getMatchedCount()) {
            return true;
        }

        return false;
    }
```

And here is the function that update the database itself.
We see that the only way this fails is if the ID is not matched to an existing object, however all the data is directly passed to the `$set` option.

Even though the website doesn't let us, we can still perform a request to update the `access` field of the user.
This is cool, since we have already seen that it is potentially a PHP serialized array, so we might have found an unsafe deserialization bug!

```php
// models/UserModel.php
    public function __construct()
    {
        parent::__construct();
        $this->username = $_SESSION['username'] ?? '';
        $this->email    = $_SESSION['email'] ?? '';
        $this->access   = unserialize($_SESSION['access'] ?? '');
        var_dump($this->access);
    }
```

And indeed each time a `UserModel` class is instantiated we see that the `access` field is read from the session and then deserialized.

```php
// controlles/AuthController.php
    public function login($router)
    {
        $username = $_POST['username'];
        $password = $_POST['password'];

        if (empty($username) || empty($password)) {
            $router->jsonify(['message' => 'Insufficient parameters!', 'status' => 'danger'], 400);
        }

        $login = $this->user->login($username, $password);

        if (empty($login)) {
            $router->jsonify(['message' => 'Wrong username or password!', 'status' => 'danger'], 400);
        }

        $_SESSION['username'] = $login->username;
        $_SESSION['access']   = $login->access;

        $router->jsonify(['message' => 'Login was successful!', 'status' => 'success']);
    }
```

And here we see that upon user login, the `access` field is fetched from the database, and then it is stored in the session.

Ok great! Now to find the PHP deserialization -> RCE...

Yeah this took quite long to find. In general PHP deserialization is not as insecure as some of the others we had during this contest.

To get RCE there needs to be some classes which have specific magic functions (`__wakeup`, `__destruct`, etc..), and on top of that the magic functions need to interact with some fields of the object that we control and somehow allow for code execution with `eval` or `system` for example.

I looked for these magic functions, however there aren't many and the few we have sets fields to `null`, or returns an element of an array as a string, not very RCE.

Upon looking more into PHP deserialization resources, I have found the [phpggc](https://github.com/ambionics/phpggc) project, which contains payloads using a more advanced technique: **POP chaining**, which I like to think of as the ROP chains of PHP deserialization.

The exploits on here contain chains that exist in specific php libraries/frameworks.
However none of the ones listed in the project appear inside of the **backend** `vendor` folder.

So are we stuck?

Not really, let's try harder.

Let's look into the `vendor` folder in the **frontend** part of the app.
Here we see a dependency that could be interesting: **monolog**

The `phpggc` project lists several chains for the dependency and many of them grant us RCE even!
Further more we know that **monolog** is pulled as a dependency for `maxbanton/cwh` from the `composer.json` file.

Upon checking the [package page](https://packagist.org/packages/maxbanton/cwh) we see that monolog 2.x is pulled, so this limits the chains we can use from `phpggc` but still we have some RCE ones.

Now to address the elephant in the room: the frontend contains no `unserialize` statement, so how are we going to to use our chain from `phpggc` if our deserialization takes place in the **backend** code?

So again, are we stuck?

Still not, keep looking a bit more!
Look no further than the `index.php` file in the backend code:

```php
require __DIR__ . "/vendor/autoload.php";

spl_autoload_register(function ($name) {
    if (preg_match('/Controller$/', $name)) {
        $name = "controllers/${name}";
    } elseif (preg_match('/Model$/', $name)) {
        $name = "models/${name}";
    } elseif (preg_match('/_/', $name)) {
        $name = preg_replace('/_/', '/', $name);
    }

    $filename = "/${name}.php";

    if (file_exists($filename)) {
        require $filename;
    }
    elseif (file_exists(__DIR__ . $filename)) {
        require __DIR__ . $filename;
    }
});
```

Interesting... this functions seems to suffer from an LFI vulnerability, however we do have a restriction for `.php` files.

But how do we call this function at all?
Turns out this function is using the *autoload* mechanism, let's read the [docs](https://www.php.net/manual/en/function.spl-autoload-register.php) of this function.

Okay, so this function replaced the deprecated `__autoload` function, which
>  Attempt to load undefined class

Great! this is exactly what we want, we have some classes we want to refer to from the frontend, and we want them to be loaded, so we can execute the POP chain that `phpggc` gives us!

However this does not automatically work, since just refering to the classes like the generated payload does, will try to look for them inside the `backend` code still.

We need to manually try and unserialize object that will cause the classes to be loaded from the frontend code.

Let's take a closer look at how the autoloading function works here
* If the class name ends in `Controller` we look inside the controllers folder for a php file with the same name as the class
* If the class name ends in `Model` we look inside the models folder for a php file with the same name as the class
* If the class name contains `_`, we replace all underscores with `/` instead
* We append `/` to the start and `.php` to the end of the parsed name
* Check if the file exists as an absolute path and load it if yes
* Check if the file exists relative to current folder and load it if yes

So by providing `_` instead of `/` we can load arbitrary php file from anywhere on the system.

Let's use this to load all the php files that give us the classes the the `phpggc` chain will use:
* `GroupHandler`
* `FingersCrossedHandler`

For my chosen exploit generated by
```shell
➜  web_unearthly_shop ./phpggc Monolog/RCE5 system "/readflag" > ./payload
```

For example an object with name `www_frontend_vendor_monolog_monolog_src_Monolog_Handler_GroupHandler` will load the `GroupHandler` class from the frontend vendor folder.

After this the class can be referred to as usual with `Monolog\Handler\GroupHandler`.

Keep in mind however that these classes have their own dependencies, that are not loaded into the current context, and will be loaded using the same function. We need to include these in advance, otherwise the exploit will fail!

Let's go over the plan one more time:
1. Login as admin using the NoSQL injection vuln
2. Change the access field of the admin to our malicious serialized payload
3. Login again as admin to trigger the deserialization

Our serialized exploit will look as follows:
* It will be an array of objects.
* The last element will be exactly the payload generated by `phpggc`
* The elements before will be objects that load dependencies from the **frontend** folder
    - these classes will specify absolute paths to php files
    - these will need to include all transitive dependencies, not just direct ones of the `phpggc` chain
* Some care needs to be taken to properly send this exploit over JSON
    - escape backslash
    - escape quotes
    - `\u0000` escape for null bytes, yes, the generated exploit contains null bytes

The full details can be seen in the `exploit.py` file, that construct the serialized string and encodes it properly for JSON transportation.

Now we just send this as the `access` variable to the endpoint that can update the user password.

After this logout, then login as admin, and see the flag :)
