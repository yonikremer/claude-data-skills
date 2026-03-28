# S3 API Reference (boto3)

## `boto3.client('s3', ...)`
Creates a low-level S3 client.

### `upload_file(Filename, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)`
Upload a file from a local path to an S3 object.

### `download_file(Bucket, Key, Filename, ExtraArgs=None, Callback=None, Config=None)`
Download an S3 object to a local file path.

### `list_objects_v2(Bucket, Prefix='', Delimiter='', MaxKeys=1000)`
Returns some or all (up to 1000) of the objects in a bucket.

### `get_object(Bucket, Key, Range=None, ...)`
Retrieves objects from Amazon S3. Returns a dictionary containing the object's metadata and a `Body` (StreamingBody).

### `put_object(Bucket, Key, Body, ...)`
Adds an object to a bucket.

### `delete_object(Bucket, Key)`
Removes the null version (if there is one) of an object and inserts a delete marker.

### `generate_presigned_url(ClientMethod, Params=None, ExpiresIn=3600, HttpMethod=None)`
Generate a presigned url given a client, its method, and arguments.

---

## `boto3.resource('s3', ...)`
Creates a higher-level S3 resource.

### `Bucket(name)`
Creates a Bucket resource.
Example: `s3.Bucket('my-bucket').objects.all()`
