# scanner/threading_utils.py

# This file handles concurrent port scanning using threading.
# It improves performance by scanning multiple ports at once.

# TODO:
# 1. Import ThreadPoolExecutor from concurrent.futures
#
# 2. Create a function scan_ports_threaded(target_ip, ports, max_threads):
#    - Use ThreadPoolExecutor with max_threads
#    - Submit scan_port tasks for each port
#    - Collect results as they complete
#    - Return a list of open ports
#
# 3. Ensure thread safety:
#    - Avoid shared mutable state issues
#
# Notes:
# - This function should call scan_port from scanner.core
# - Do not duplicate scanning logic here