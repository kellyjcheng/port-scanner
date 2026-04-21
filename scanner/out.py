import json
import csv
from datetime import datetime


def _default_filename(fmt):
    """
    Behavior: Generates a timestamped default filename for scan output files so
              successive scans do not overwrite each other.
    Parameters:
        fmt (str): File format extension, e.g. "json", "csv", or "txt".
    Returns:
        str: A filename string such as "scan_results_20260420_153012.json".
    Exceptions:
        None raised.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"scan_results_{ts}.{fmt}"


def save_results_json(target, results, filename=None):
    """
    Behavior: Serialises the scan results to a JSON file. Each entry in results
              is written as-is; the file also records the target address and the
              timestamp at which the export was performed.
    Parameters:
        target  (str):        The scanned IPv4 address.
        results (list[dict]): List of dicts, each with keys "port" (int),
                              "service" (str), and optionally "banner" (str|None).
        filename (str|None):  Output filepath. Defaults to a timestamped name in
                              the current working directory.
    Returns:
        str: The path of the file that was written.
    Exceptions:
        OSError: Raised if the file cannot be opened for writing.
    """
    filename = filename or _default_filename("json")
    data = {
        "target": target,
        "scanned_at": datetime.now().isoformat(timespec="seconds"),
        "open_ports": results,
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Results saved to {filename}")
    return filename


def save_results_csv(target, results, filename=None):
    """
    Behavior: Writes scan results to a CSV file with columns: port, service,
              and banner. A header row is always written first. Rows with no
              banner value are written with an empty string in that column.
    Parameters:
        target  (str):        The scanned IPv4 address (written as a comment in
                              the first row).
        results (list[dict]): List of dicts, each with keys "port", "service",
                              and optionally "banner".
        filename (str|None):  Output filepath. Defaults to a timestamped name.
    Returns:
        str: The path of the file that was written.
    Exceptions:
        OSError: Raised if the file cannot be opened for writing.
    """
    filename = filename or _default_filename("csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# target", target])
        writer.writerow(["port", "service", "banner"])
        for r in results:
            writer.writerow([r["port"], r["service"], r.get("banner") or ""])
    print(f"[+] Results saved to {filename}")
    return filename


def save_results_txt(target, results, filename=None):
    """
    Behavior: Writes a human-readable plain-text report of open ports. Each line
              follows the format "[OPEN] <port>/tcp → <service>  <banner>".
              Banner text is included only when present.
    Parameters:
        target  (str):        The scanned IPv4 address.
        results (list[dict]): List of dicts, each with keys "port", "service",
                              and optionally "banner".
        filename (str|None):  Output filepath. Defaults to a timestamped name.
    Returns:
        str: The path of the file that was written.
    Exceptions:
        OSError: Raised if the file cannot be opened for writing.
    """
    filename = filename or _default_filename("txt")
    with open(filename, "w") as f:
        f.write(f"Scan target : {target}\n")
        f.write(f"Scanned at  : {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"Open ports  : {len(results)}\n")
        f.write("-" * 60 + "\n")
        for r in results:
            banner_str = f"  {r['banner']}" if r.get("banner") else ""
            f.write(f"[OPEN] {r['port']:>5}/tcp  →  {r['service']}{banner_str}\n")
    print(f"[+] Results saved to {filename}")
    return filename


def export_results(target, results, fmt, filename=None):
    """
    Behavior: Dispatches to the appropriate format-specific save function based
              on the fmt argument. Acts as the single public entry point for all
              export operations.
    Parameters:
        target   (str):        The scanned IPv4 address.
        results  (list[dict]): List of dicts, each with keys "port", "service",
                               and optionally "banner".
        fmt      (str):        Export format — one of "json", "csv", or "txt".
        filename (str|None):   Optional output filepath override.
    Returns:
        str: The path of the file that was written.
    Exceptions:
        ValueError: Raised when fmt is not one of the supported values.
        OSError:    Raised by the underlying save function if the file cannot
                    be opened for writing.
    """
    dispatch = {
        "json": save_results_json,
        "csv":  save_results_csv,
        "txt":  save_results_txt,
    }
    if fmt not in dispatch:
        raise ValueError(f"Unsupported export format '{fmt}'. Choose from: json, csv, txt.")
    return dispatch[fmt](target, results, filename)


# Keep the original simple function as an alias for backward compatibility.
def save_results(target, open_ports):
    """
    Behavior: Convenience wrapper that converts a plain list of port integers
              into the richer results format and delegates to save_results_json.
              Retained for backward compatibility with callers that pass a raw
              port list.
    Parameters:
        target     (str):       The scanned IPv4 address.
        open_ports (list[int]): List of open port numbers.
    Returns:
        str: The path of the JSON file that was written.
    Exceptions:
        OSError: Raised if the file cannot be opened for writing.
    """
    results = [{"port": p, "service": "Unknown", "banner": None} for p in open_ports]
    return save_results_json(target, results, filename="scan_results.json")
