# Trap Track (hard)
In this challenge we will use SSRF and unsafe deserialization in python to get the flag.

This time the login page is easily bypassed, since we know from `config.py` that admin username and password is the same.

Once we are logged in we can see that list of websites, healthcheck and the status.
We can add websites, then they are going go to a queue of some sort, then be checked and then finally the job is considered completed.

Let's inspect how this works in the source code:
```python
# blueprints/routes.py:59
    data = request.get_json()

    trapName = data.get('trapName', '')
    trapURL = data.get('trapURL', '')

    if not trapName or not trapURL:
        return response('Missing required parameters!', 401)

    async_job = create_job_queue(trapName, trapURL)

    track = TrapTracks(trap_name=trapName, trap_url=trapURL, track_cron_id=async_job['job_id'])

    db.session.add(track)
    db.session.commit()

    return response('Trap Track added successfully!', 200)
```

First a *job queue* is created, and then the track is added to a database.

```python
# cache.py:22
def create_job_queue(trapName, trapURL):
    job_id = get_job_id()

    data = {
        'job_id': int(job_id),
        'trap_name': trapName,
        'trap_url': trapURL,
        'completed': 0,
        'inprogress': 0,
        'health': 0
    }

    current_app.redis.hset(env('REDIS_JOBS'), job_id, base64.b64encode(pickle.dumps(data)))

    current_app.redis.rpush(env('REDIS_QUEUE'), job_id)

    return data
```

It seems like the job gets added to to `REDIS_JOBS` and then the job id gets pushed to the queue.
Okay here we see something interesting, the data is serialized with `pickle` and then `base64` encoded.
A bit below in the same file we see something even more exciting:

```python
def get_job_queue(job_id):
    data = current_app.redis.hget(env('REDIS_JOBS'), job_id)
    if data:
        return pickle.loads(base64.b64decode(data))

    return None
```

The data from the job, just gets loaded, `base64` decoded and then `pickle` deserialized.
Awesome if we could only control what is that data of this job, then we could exploit this deserialization bug to get RCE, and then get the flag!

Going through official means of adding a job, seem to add useless attributes that we do not want. We need to find a way to add jobs without this restriction.

But so far we haven't even looked what a job is, or how it gets executed!

For this we have to go outside the `application` folder and look into the `worker` folder.

```python
# main.py:43
def run_worker():
    job = get_work_item()
    if not job:
        return

    incr_field(job, 'inprogress')

    trapURL = job['trap_url']

    response = request(trapURL)

    set_field(job, 'health', 1 if response else 0)

    incr_field(job, 'completed')
    decr_field(job, 'inprogress')
```

Okay, we get the jobs from the redis queue, then modify some state, let's look into this `request` function!

```python
# healthcheck.py
import pycurl

def request(url):
    response = False
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.TIMEOUT, 5)
        c.setopt(c.VERBOSE, True)
        c.setopt(c.FOLLOWLOCATION, True)

        response = c.perform_rb().decode('utf-8', errors='ignore')
        c.close()
    finally:
        return response
```

We send a request using curl to the url that is specified in the job.
But we have control over this URL, right? And here is the SSRF vuln.

Now we can use this vuln in order to communicate with the redis backend.
How this exactly happens took some research to figure out, however I stumbled upon this [article](https://maxchadwick.xyz/blog/ssrf-exploits-against-redis)

Using the *gopher* protocol in curl makes it easy to send commands to the redis backend.

Now all that is left to do is to craft the pickle exploit and the proper URL which when loaded by curl will trigger the redis command.

This is done by `exploit.py`, whichr returns an URL we can use when adding a new job.

The exploit will create a job with ID 1337.
However we are not fully done yet, we still need to force the deserialization, which we can do by requesting the `/tracks/1337/status` endpoint.

```python
# blueprints/routes.py
@api.route('/tracks/<int:job_id>/status', methods=['GET'])
@login_required
def job_status(job_id):
    data = get_job_queue(job_id)

    if not data:
        return response('Job does not exist!', 401)

    return Response(json.dumps(data), mimetype='application/json')
```

This will call `get_job_queue` which we alread know deserializes the job data.
