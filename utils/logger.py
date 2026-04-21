# utils/logger.py

from colorama import Fore, Style, init

init(autoreset=True)


def log_info(message):
    """
    Behavior: Prints an informational message to stdout with a neutral [*] prefix.
    Parameters:
        message (str): The message to display.
    Returns:
        None
    Exceptions:
        None raised.
    """
    print(f"{Style.BRIGHT}[*]{Style.RESET_ALL} {message}")


def log_success(message):
    """
    Behavior: Prints a success message to stdout in green with a [+] prefix.
    Parameters:
        message (str): The message to display.
    Returns:
        None
    Exceptions:
        None raised.
    """
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {message}")


def log_error(message):
    """
    Behavior: Prints an error message to stdout in red with a [-] prefix.
    Parameters:
        message (str): The message to display.
    Returns:
        None
    Exceptions:
        None raised.
    """
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {message}")


def log_open_port(port, service="Unknown", banner=None):
    """
    Behavior: Prints a formatted open-port result line in cyan. The output always
              includes the port number and service name. When a banner string is
              provided it is appended on the same line after a separator.
    Parameters:
        port    (int):      The open port number.
        service (str):      Human-readable service name (default: "Unknown").
        banner  (str|None): Optional banner text received from the service.
    Returns:
        None
    Exceptions:
        None raised.
    """
    banner_str = f"  |  {banner}" if banner else ""
    print(f"{Fore.CYAN}[OPEN]{Style.RESET_ALL} {port:>5}/tcp  →  {service}{banner_str}")
