# scanner/core.py

# This file contains the core port scanning logic using sockets.
# It should NOT handle threading or CLI input.

# TODO:
# 1. Create a function scan_port(target_ip, port):
#    - Create a TCP socket
#    - Set a timeout (from config.settings)
#    - Attempt to connect using socket.connect_ex()
#    - Return True if port is open, False otherwise
#
# 2. Create a function scan_ports_sequential(target_ip, ports):
#    - Loop through a list of ports
#    - Call scan_port for each
#    - Collect and return a list of open ports
#
# Notes:
# - Keep this file simple and focused
# - Do not print results here (return data instead)