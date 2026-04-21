# scanner/banner.py

# This file handles banner grabbing from open ports.
# Banner grabbing helps identify services running on a port.

# TODO:
# 1. Create a function grab_banner(target_ip, port):
#    - Open a socket connection to the port
#    - Send a simple request if needed (e.g., HTTP GET)
#    - Attempt to receive data from the server
#    - Return the banner string (or None if unavailable)
#
# 2. Handle exceptions:
#    - Timeout
#    - Connection reset
#
# Notes:
# - This is optional but adds strong cybersecurity relevance
# - Keep it separate from core scanning logic