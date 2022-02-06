"""Make GET requests asynchronously.

This module uses only the low-level asyncio transport and protocol for
TCP connections, no third-party library is used.

"""

import asyncio
from typing import Optional


__all__ = ("get_request", "get_requests")

class _ClientProtocol(asyncio.Protocol):
    """Protocol to handle the client communication.

    Note:
        All methods are callbacks - they are called by the coupled
        transport on certain events.

    Attributes:
        message: The encoded message to send to the server.
        on_con_lost: Future to signal that the connection has been
            closed by the server so that we can gracefully close the
            transport.
        payload: Reference to a bytearray to which the received payload
            from the server will be added.

    """
    def __init__(self, message: bytes, on_con_lost: asyncio.Future, payload: bytearray):
        self.message = message
        self.on_con_lost = on_con_lost

        # Reference to payload object so that the actual payload is
        # stored outside of this object.
        self.payload = payload

    def connection_made(self, transport: asyncio.Transport):
        transport.write(self.message)

    def data_received(self, data: bytes):
        # NOTE: Only add to the payload as it is a reference to an
        # "external" object.
        self.payload += data

    def connection_lost(self, exc):
        # The server closed the connection.
        self.on_con_lost.set_result(True)


async def get_request(
    host: str,
    port: int,
    loop: asyncio.AbstractEventLoop,
) -> bytearray:
    """Make a GET request."""
    def protocol_factory() -> _ClientProtocol:
        nonlocal message, on_con_lost, payload
        return _ClientProtocol(message, on_con_lost, payload)

    on_con_lost = loop.create_future()
    message = b"GET / HTTP/1.0\r\n\r\n"  # GET request
    payload = bytearray()

    transport, _ = await loop.create_connection(protocol_factory, host, port)

    # Wait until the protocol signals that the connection is lost and
    # close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()

    return payload


async def get_requests(
    urls: list[tuple[str, int]],
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> tuple[bytearray]:
    """Make a GET request for every url in urls asynchronously.

    Args:
        urls: Urls to make the GET request to. Example:

            [("google.com", 80"), ("example.org", 80)]

        loop: Reference to the event loop. If `None` is given, then
            `asyncio.get_running_loop()` is used to obtain the
            reference.

    """
    # Get a reference to the event loop as aioreq uses low-level APIs.
    if loop is None:
        loop = asyncio.get_running_loop()

    aws = [
        get_request(host, port, loop)
        for host, port in urls
    ]
    return await asyncio.gather(*aws)
