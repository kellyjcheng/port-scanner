# scanner/banner.py

import socket
from config.settings import DEFAULT_TIMEOUT


def grab_banner(ip, port):
    """
    Behavior: Opens a TCP socket connection to ip:port and attempts to receive
              up to 1024 bytes of data that the service sends on connect (its
              banner). The received bytes are decoded leniently so non-UTF-8
              bytes are replaced rather than raising an error. The socket is
              always closed after the attempt.
    Parameters:
        ip   (str): The IPv4 address of the target host.
        port (int): The open port from which to read a banner.
    Returns:
        str | None: The stripped banner string if any data is received, or None
                    if the connection times out, is refused, is reset, or the
                    service sends no data.
    Exceptions:
        None raised; all socket exceptions are caught internally.
    """
    try:
        s = socket.socket()
        s.settimeout(DEFAULT_TIMEOUT)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors="ignore")
        s.close()
        return banner.strip() or None
    except Exception:
        return None
