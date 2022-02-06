"""Example HTTP server that can handle multiple clients concurrently.

Example server that handles up to NUM_CLIENTS concurrent connections by
using a ThreadPool. Run the server using:

    python examples/server.py

"""

import socket
import time
from concurrent.futures import ThreadPoolExecutor


HOST = "localhost"
PORT = 5000
NUM_CLIENTS = 10

# Example HTTP response a server could send.
HTTP_OK_RESPONSE = b"""
HTTP/1.0 200 OK
Content-type: text/html
Content-Length: 70

<!DOCTYPE html>
<html>
<body>

<h1>HELLO WORLD!</h1>

</body>
</html>
"""


def handle_conn(conn: socket.socket, addr) -> None:
    with conn:
        print("Connected by", addr)
        _ = conn.recv(1024)

        # Mimic a CPU intensive task.
        time.sleep(3)

        conn.sendall(HTTP_OK_RESPONSE)

    print("Done handling", addr)


def main() -> None:
    # Listen for incoming connections.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Serve requests indefinitely, each within its own thread.
        with ThreadPoolExecutor(max_workers=NUM_CLIENTS) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_conn, conn, addr)


if __name__ == "__main__":
    main()
