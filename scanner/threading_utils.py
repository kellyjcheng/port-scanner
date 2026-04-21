# scanner/threading_utils.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.core import scan_port


def scan_ports_threaded(target_ip, ports, max_threads):
    """
    Behavior: Distributes port-scanning work across a thread pool so multiple
              ports are probed concurrently. Each worker calls scan_port and
              results are collected via as_completed as futures finish. Thread
              safety is maintained by building the result list only from
              immutable future return values — no shared mutable state is used.
    Parameters:
        target_ip (str): The IPv4 address of the target host.
        ports (iterable of int): The ports to scan.
        max_threads (int): Maximum number of concurrent threads in the pool.
    Returns:
        list[int]: Sorted list of open port numbers found during the scan.
    Exceptions:
        None raised; exceptions within individual scan_port calls are handled
        internally by scan_port and cause that port to be treated as closed.
    """
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port): port for port in ports}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
    return sorted(open_ports)
