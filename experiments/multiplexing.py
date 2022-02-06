"""Asynchronous requests using I/O multiplexing using select.

Calls s.recv() the moment the socket is ready to be read from instead
of waiting until data is received and thereby blocking the thread.

Note:
    Of course there are also other blocking operations that can be
    removed by using the asyncio socket abstraction, e.g. creating
    the connection. For this checkout experiments/asyncio_sockets.py

Run a server to test it out:

    python examples/server.py

This script will also run in about 6s.

"""
import select
import socket


HOST = "127.0.0.1"  # localhost
PORT = 5000
NUM_REQUESTS = 20

# File descriptors (in our case sockets) that are not ready yet to
# be read from.
_read_wait = { }

def get_request(host: str, port: int) -> None:
    # Don't close the socket (and so don't use a context manager)
    # because we will later read from the socket.
    s = socket.create_connection((host, port))

    s.sendall(b"GET / HTTP/1.0\r\n\r\n")
    _read_wait[s] = s.recv


def main() -> None:
    # Make a number of request synchronously.
    for _ in range(NUM_REQUESTS):
        get_request(HOST, PORT)

    # Handle the response, i.e. the `recv()` call, asynchronously.
    num_select_calls = 0
    while _read_wait:
        # Get an iterable containing the file descriptors that are read
        # ready.
        can_read, _, _ = select.select(_read_wait, [], [])
        num_select_calls += 1

        for fd in can_read:
            # Use a context manager so that the socket is closed.
            with fd:
                func = _read_wait.pop(fd)

                # We don't care about the data in this experiment.
                func(1024)  # invokes the `recv()`

                print("GET request response received.")

    print("Number of `select()` calls:", num_select_calls)


if __name__ == "__main__":
    main()
