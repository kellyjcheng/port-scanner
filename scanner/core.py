# scanner/core.py

import socket
from config.settings import DEFAULT_TIMEOUT


def scan_port(target_ip, port):
    """
    Behavior: Opens a TCP socket, sets a timeout, and attempts a non-blocking
              connect to target_ip:port via connect_ex. The socket is closed
              immediately after the attempt regardless of outcome.
    Parameters:
        target_ip (str): The IPv4 address of the target host.
        port (int): The port number to probe.
    Returns:
        bool: True if the port is open (connect_ex returns 0), False otherwise.
    Exceptions:
        None raised; socket.error is caught internally and returns False.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(DEFAULT_TIMEOUT)
            return sock.connect_ex((target_ip, port)) == 0
    except socket.error:
        return False


def scan_ports_sequential(target_ip, ports):
    """
    Behavior: Iterates over the provided port list and calls scan_port for each,
              collecting every port that responds as open. Results are returned
              in sorted order.
    Parameters:
        target_ip (str): The IPv4 address of the target host.
        ports (iterable of int): The ports to scan.
    Returns:
        list[int]: Sorted list of open port numbers.
    Exceptions:
        None raised; individual port errors are handled within scan_port.
    """
    open_ports = [port for port in ports if scan_port(target_ip, port)]
    return sorted(open_ports)
