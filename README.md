
# io_reader

Basic Flask API implementation in Python for a IO file reader.

# API Description

## Overview

This API provides an endpoint to retrieve the I/O counter state of a specific process on a Unix-like system. It is built using the Flask web framework.

## Base URL

`http://<your-server-domain>/`

## Endpoints

### Get Counter State of a Process

* __Endpoint__: `/counter_state/<int:pid>`
* __Method__: `GET`
* __Description__: Retrieves the I/O counter state for a process identified by its process ID (PID).
* __Path Parameters__:
pid (integer): The process ID of the process whose I/O counter state is to be retrieved.
* __Responses__:
  * __200 OK__: Returns the I/O counter state of the specified process.
  * __403 Forbidden__: Permission denied to access the `/proc/<pid>/io` file.
  * __404 Not Found__: The `/proc/<pid>/io` file does not exist.
  * __422 Unprocessable Entity__:
    * Key not found in file content.
    * Invalid content in `/proc/<pid>/io`.

__Example Request:__

``` bash
GET /counter_state/1234 HTTP/1.1
Host: <your-server-domain>
```

__Example Response:__

``` bash
{
  "write_bytes": 1024,
  "read_bytes": 2048
}
```

__Error Responses:__

__* 403 Forbidden:__

```json
{
"description": "Permission denied to /proc/1234/io"
}
```

__* 404 Not Found:__

``` json
{
"description": "/proc/1234/io not found"
}
```

__* 422 Unprocessable Entity:__

``` json
{
"description": "Key 'some_key' not found in file content"
}
```

or

``` json
{
"description": "Invalid content in /proc/1234/io"
}
```

### Notes:
* The `FILE_PATH` environment variable can be set to customize the path template for the process I/O file. 
The default path is `/proc/<pid>/io.`
* The `IOFile` class represents the number of bytes read and written by a process.

## Thoughts

* No point of caching if the values changes likely every call

### Extension ideas
* Golang
* Using Django 
* Using FastAPI
