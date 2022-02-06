"""Asynchronous requests using asyncio with sockets.

From the Python docs:
> Working with sockets directly is slower than using the protocol
> implementation that use transport-based APIs.

Run a server to test it out:

    python examples/server.py

This script will also run in about 6s.

"""
import asyncio
import socket


HOST = "127.0.0.1"  # localhost
PORT = 5000
NUM_REQUESTS = 20

async def get_request(host: str, port: int, loop: asyncio.AbstractEventLoop) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Make the socket non-blocking as otherwise the system calls for
        # `send()`, `recv()`, `connect()` and `accept()` would all be
        # blocking still.
        s.setblocking(False)

        await loop.sock_connect(s, (host, port))
        await loop.sock_sendall(s, b"GET / HTTP/1.0\r\n\r\n")

        # We don't care about the data in this experiment.
        await loop.sock_recv(s, 1024)

    print("GET request response received.")


async def main():
    loop = asyncio.get_event_loop()
    aws = [
        get_request(HOST, PORT, loop)
        for _ in range(NUM_REQUESTS)
    ]
    await asyncio.gather(*aws)


if __name__ == "__main__":
    asyncio.run(main())
