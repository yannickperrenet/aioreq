"""Synchronous requests using a socket directly.

Run a server to test it out:

    python examples/server.py

This script will run in about 60s.

"""
import socket

HOST = "127.0.0.1"  # localhost
PORT = 5000
NUM_REQUESTS = 20

def get_request(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"GET / HTTP/1.0\r\n\r\n")

        # NOTE: This call will be noticeably blocking as it will wait
        # until it has received a response from the server.
        s.recv(1024)

    print("GET request response received.")


def main():
    for _ in range(NUM_REQUESTS):
        get_request(HOST, PORT)


if __name__ == "__main__":
    main()
