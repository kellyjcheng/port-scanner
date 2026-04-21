# main.py

import argparse
import sys

from config.settings import DEFAULT_START_PORT, DEFAULT_END_PORT, DEFAULT_THREADS
from utils.validators import is_valid_ip, validate_port_range
from utils.logger import log_info, log_success, log_error, log_open_port
from scanner.threading_utils import scan_ports_threaded
from scanner.banner import grab_banner
from scanner.services import get_service
from scanner.out import export_results

# Preset port ranges and thread counts for each scan mode.
SCAN_MODES = {
    "quick":   {"start": 1,  "end": 1024,  "threads": 200},
    "full":    {"start": 1,  "end": 65535, "threads": 100},
    "stealth": {"start": 1,  "end": 1024,  "threads": 5},
}


def parse_args():
    """
    Behavior: Defines and parses CLI arguments for the port scanner. When --mode
              is given its preset values fill in any omitted --start, --end, or
              --threads arguments. Explicit flag values always take precedence over
              the mode preset.
    Parameters:
        None
    Returns:
        argparse.Namespace: Parsed argument object with attributes: target (str),
                            start (int), end (int), threads (int), mode (str|None),
                            banners (bool), and export (str|None).
    Exceptions:
        SystemExit: Raised by argparse on missing required args or --help.
    """
    parser = argparse.ArgumentParser(
        description="Python port scanner — TCP connect scan with service ID, banner grabbing, and export."
    )
    parser.add_argument(
        "--target", required=True,
        help="Target IPv4 address to scan."
    )
    parser.add_argument(
        "--mode", choices=SCAN_MODES.keys(), default=None,
        help=(
            "Scan mode preset. quick=1-1024 (200 threads), "
            "full=1-65535 (100 threads), stealth=1-1024 (5 threads, slow). "
            "Explicit --start/--end/--threads override the preset."
        )
    )
    parser.add_argument(
        "--start", type=int, default=None,
        help=f"Start of port range (default: {DEFAULT_START_PORT}, or set by --mode)."
    )
    parser.add_argument(
        "--end", type=int, default=None,
        help=f"End of port range (default: {DEFAULT_END_PORT}, or set by --mode)."
    )
    parser.add_argument(
        "--threads", type=int, default=None,
        help=f"Number of threads (default: {DEFAULT_THREADS}, or set by --mode)."
    )
    parser.add_argument(
        "--banners", action="store_true",
        help="Attempt to grab service banners from each open port."
    )
    parser.add_argument(
        "--export", choices=["json", "csv", "txt"], default=None,
        help="Export results to a timestamped file in the chosen format."
    )
    return parser.parse_args()


def resolve_scan_params(args):
    """
    Behavior: Merges the --mode preset with any explicitly provided --start,
              --end, and --threads flags. Explicit flags always win over the
              preset; config defaults are used when neither is supplied.
    Parameters:
        args (argparse.Namespace): Parsed CLI arguments from parse_args().
    Returns:
        tuple[int, int, int]: A (start, end, threads) triple ready for use.
    Exceptions:
        None raised.
    """
    preset = SCAN_MODES.get(args.mode, {})
    start   = args.start   if args.start   is not None else preset.get("start",   DEFAULT_START_PORT)
    end     = args.end     if args.end     is not None else preset.get("end",     DEFAULT_END_PORT)
    threads = args.threads if args.threads is not None else preset.get("threads", DEFAULT_THREADS)
    return start, end, threads


def main():
    """
    Behavior: Entry point for the CLI tool. Resolves scan parameters, validates
              inputs, runs a threaded scan, looks up each open port's service name,
              optionally grabs banners, prints results via the logger, and exports
              to file when --export is specified.
    Parameters:
        None
    Returns:
        None
    Exceptions:
        SystemExit: Exit code 1 on invalid input; exit code 0 on KeyboardInterrupt.
    """
    args = parse_args()
    start, end, threads = resolve_scan_params(args)

    if not is_valid_ip(args.target):
        log_error(f"Invalid IP address: {args.target}")
        sys.exit(1)

    if not validate_port_range(start, end):
        log_error(
            f"Invalid port range: {start}–{end}. "
            "Ports must be 1–65535 and start must be <= end."
        )
        sys.exit(1)

    mode_label = f" [{args.mode} mode]" if args.mode else ""
    log_info(
        f"Scanning {args.target} — ports {start}–{end} "
        f"using {threads} threads{mode_label}..."
    )

    try:
        open_ports = scan_ports_threaded(args.target, range(start, end + 1), threads)
    except KeyboardInterrupt:
        log_error("Scan aborted by user.")
        sys.exit(0)

    if not open_ports:
        log_info("No open ports found.")
        return

    log_success(f"Found {len(open_ports)} open port(s):\n")

    results = []
    for port in open_ports:
        service = get_service(port)
        banner  = grab_banner(args.target, port) if args.banners else None
        results.append({"port": port, "service": service, "banner": banner})
        log_open_port(port, service, banner)

    if args.export:
        export_results(args.target, results, args.export)


if __name__ == "__main__":
    main()
