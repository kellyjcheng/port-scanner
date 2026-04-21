# main.py

# This is the entry point for the port scanner CLI tool.
# Responsibilities:
# - Parse command-line arguments (target IP, port range, optional flags)
# - Validate user input using utils.validators
# - Call scanning functions from scanner.core or scanner.threading_utils
# - Display results in a clean format (optionally using utils.logger)

# TODO:
# 1. Use argparse to define CLI arguments:
#    --target (required): target IP address
#    --start (optional): start port (default from config)
#    --end (optional): end port (default from config)
#    --threads (optional): number of threads to use
#
# 2. Validate inputs:
#    - Check if IP is valid
#    - Ensure port range is within 1–65535
#
# 3. Call threaded scanning function:
#    - Pass target and port range
#    - Receive list of open ports
#
# 4. Print results:
#    - Show open ports clearly
#    - Optionally format output (clean spacing or table)
#
# 5. Handle errors gracefully (invalid input, connection issues)