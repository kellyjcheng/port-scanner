# main.py

import argparse
import sys

from config.settings import DEFAULT_START_PORT, DEFAULT_END_PORT, DEFAULT_THREADS
from utils.validators import is_valid_ip, validate_port_range
from utils.logger import log_info, log_success, log_error
from scanner.threading_utils import scan_ports_threaded
from scanner.banner import grab_banner


def parse_args():
    """
    Behavior: Defines and parses CLI arguments for the port scanner using argparse.
              --target is required; --start, --end, and --threads fall back to
              defaults from config.settings when omitted.
    Parameters:
        None
    Returns:
        argparse.Namespace: Parsed argument object with attributes target (str),
                            start (int), end (int), threads (int), and banners (bool).
    Exceptions:
        SystemExit: Raised by argparse when required arguments are missing or
                    --help is requested.
    """
    parser = argparse.ArgumentParser(
        description="Python port scanner — fast TCP connect scan with optional banner grabbing."
    )
    parser.add_argument(
        "--target", required=True,
        help="Target IPv4 address to scan."
    )
    parser.add_argument(
        "--start", type=int, default=DEFAULT_START_PORT,
        help=f"Start of port range (default: {DEFAULT_START_PORT})."
    )
    parser.add_argument(
        "--end", type=int, default=DEFAULT_END_PORT,
        help=f"End of port range (default: {DEFAULT_END_PORT})."
    )
    parser.add_argument(
        "--threads", type=int, default=DEFAULT_THREADS,
        help=f"Number of threads to use (default: {DEFAULT_THREADS})."
    )
    parser.add_argument(
        "--banners", action="store_true",
        help="Attempt to grab service banners from each open port."
    )
    return parser.parse_args()


def main():
    """
    Behavior: Entry point for the CLI tool. Validates the target IP and port range,
              runs a threaded port scan, and prints results via the logger. When
              --banners is passed, also attempts banner grabbing on each open port.
    Parameters:
        None
    Returns:
        None
    Exceptions:
        SystemExit: Raised with exit code 1 on invalid input, or exit code 0 on
                    KeyboardInterrupt so the terminal is left in a clean state.
    """
    args = parse_args()

    if not is_valid_ip(args.target):
        log_error(f"Invalid IP address: {args.target}")
        sys.exit(1)

    if not validate_port_range(args.start, args.end):
        log_error(
            f"Invalid port range: {args.start}–{args.end}. "
            "Ports must be 1–65535 and start must be <= end."
        )
        sys.exit(1)

    ports = range(args.start, args.end + 1)
    log_info(
        f"Scanning {args.target} — ports {args.start}–{args.end} "
        f"using {args.threads} threads..."
    )

    try:
        open_ports = scan_ports_threaded(args.target, ports, args.threads)
    except KeyboardInterrupt:
        log_error("Scan aborted by user.")
        sys.exit(0)

    if not open_ports:
        log_info("No open ports found.")
        return

    log_success(f"Found {len(open_ports)} open port(s):\n")
    for port in open_ports:
        if args.banners:
            banner = grab_banner(args.target, port)
            banner_str = f"  {banner}" if banner else "  (no banner)"
            log_success(f"Port {port:>5}/tcp  OPEN{banner_str}")
        else:
            log_success(f"Port {port:>5}/tcp  OPEN")


if __name__ == "__main__":
    main()
