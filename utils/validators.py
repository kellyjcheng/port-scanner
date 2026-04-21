# utils/validators.py

import socket


def is_valid_ip(ip):
    """
    Behavior: Checks whether the given string is a valid IPv4 address by
              attempting to parse it with socket.inet_aton.
    Parameters:
        ip (str): The IP address string to validate.
    Returns:
        bool: True if the string is a valid IPv4 address, False otherwise.
    Exceptions:
        None raised; socket.error is caught internally and returns False.
    """
    try:
        socket.inet_aton(ip)
        return ip.count('.') == 3
    except socket.error:
        return False


def is_valid_port(port):
    """
    Behavior: Checks whether the given value is a valid port number (1–65535).
    Parameters:
        port (int): The port number to validate.
    Returns:
        bool: True if port is an integer between 1 and 65535 inclusive, False otherwise.
    Exceptions:
        None raised; TypeError and ValueError are caught internally and return False.
    """
    try:
        return 1 <= int(port) <= 65535
    except (TypeError, ValueError):
        return False


def validate_port_range(start, end):
    """
    Behavior: Validates that both start and end are valid port numbers and that
              start is less than or equal to end.
    Parameters:
        start (int): The first port in the range.
        end (int): The last port in the range.
    Returns:
        bool: True if both ports are valid and start <= end, False otherwise.
    Exceptions:
        None raised; delegates to is_valid_port which handles type errors internally.
    """
    return is_valid_port(start) and is_valid_port(end) and int(start) <= int(end)
