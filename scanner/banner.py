# scanner/banner.py

import socket
from config.settings import DEFAULT_TIMEOUT


def grab_banner(target_ip, port):
    """
    Behavior: Connects to target_ip:port and attempts to read a service banner.
              For port 80 an HTTP HEAD request is sent first to elicit a response;
              for all other ports the socket listens immediately after connecting.
              Received bytes are decoded as UTF-8 (with replacement for invalid
              bytes) and stripped of surrounding whitespace.
    Parameters:
        target_ip (str): The IPv4 address of the target host.
        port (int): The open port from which to grab a banner.
    Returns:
        str | None: The decoded banner string if data is received, or None if the
                    connection times out, is reset, returns no data, or fails.
    Exceptions:
        None raised; socket.timeout, ConnectionResetError, and socket.error are
        caught internally and cause the function to return None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(DEFAULT_TIMEOUT)
            sock.connect((target_ip, port))
            if port == 80:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024)
            return banner.decode("utf-8", errors="ignore").strip() or None
    except (socket.timeout, ConnectionResetError, socket.error):
        return None
