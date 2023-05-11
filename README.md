> This is an **educational package** (for myself) and has very limited practical use cases, if any.

# aioreq

Minimal performant package to asynchronously make GET requests **without any dependencies** other than
`asyncio` (from the standard library).

My goal for this project was to:
* Learn about asynchronous code in a practical manner.
* Build a small package that allows you to send multiple requests asynchronously using low-level
  primitives, i.e. not using any third-party package such as
  [aiohttp](https://github.com/aio-libs/aiohttp).

## Example
Check out [examples/client.py](examples/client.py) on how to use this package. It is as simple as:

```python
import asyncio
import aioreq

async def main():
    urls = [("example.org", 80), ...]
    return await aioreq.get_requests(urls)

asyncio.run(main())
```

## Practical use cases of this package
What you **can** do:
* Handle requests asynchronously without any third-party library.
* `GET` requests only
* `HTTP` requests only
* Get the payload as bytes after the connection has been closed. This payload will also include
  `HTTP` headers.

Basically all advanced things, you **can not** do using this package. Even basic things like `POST`
requests are not implemented.


## Understanding what is going on
From basic principles (synchronous requests) to a package to handle requests asynchronously without
any third-party library:
1. [experiments/synchronous_client.py](experiments/synchronous_client.py) - sync.
2. [experiments/multiplexing.py](experiments/multiplexing.py) - async.
3. [experiments/asyncio_sockets.py](experiments/asyncio_sockets.py) - async.
4. [examples/client.py](examples/client.py) - async.


## Resources
Some resources I have found extremely usefull in the process of developing this small package:
* [Build your own async](https://gist.github.com/dabeaz/f86ded8d61206c757c5cd4dbb5109f74) by David Beazly
* [`get_running_loop()`](https://github.com/python/cpython/blob/3.10/Lib/asyncio/events.py#L694)
  implementation in Python - showing that there can only be one eventloop per thread.
* [Non-blocking sockets](https://www.scottklement.com/rpg/socktut/nonblocking.html) write-up.
