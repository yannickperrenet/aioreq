"""Example of how to use aioreq.

To run this code, you first need to make sure there is a server running
at the defined HOST and PORT. Note that this server is able to serve
multiple requests concurrently. Simply run:

    python examples/server.py

Then invoke this script:

    time python examples/client.py

In the provided example we send NUM_REQUESTS and the example server can
handle NUM_CLIENTS concurrently, meaning that it is expected that this
script runs in:

    NUM_REQUESTS / NUM_CLIENTS * time to serve request

which will be a little over 6s in total.

"""

import aioreq
import asyncio


HOST = "127.0.0.1"  # localhost
PORT = 5000
NUM_REQUESTS = 20


def print_payloads(payloads: tuple[bytearray]) -> None:
    for p in payloads:
        print(p.decode("utf-8"))
        print("#--------------------------------------------------")


async def main() -> None:
    # Create some URLs to GET from.
    urls = [(HOST, PORT) for _ in range(NUM_REQUESTS)]
    await aioreq.get_requests(urls)

    print("All GET request responses received.")


if __name__ == "__main__":
    asyncio.run(main())
