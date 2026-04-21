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
