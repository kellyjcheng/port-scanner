# Port Scanner (Python Network Recon Tool)

A modular network reconnaissance tool built in Python that performs multi-threaded TCP port scanning, service detection, and optional banner grabbing. The project is designed to replicate core functionality of professional tools such as Nmap in a simplified and educational architecture.

---

## Features

- Multi-threaded TCP port scanning for improved performance
- Configurable scan ranges (fast, full, stealth modes)
- Service identification based on common port mappings
- Banner grabbing for open ports (where available)
- Command-line interface using argparse
- Structured JSON output for scan results
- Modular codebase designed for extensibility

---

## Project Structure

```text
port-scanner/
│
├── main.py
├── scanner/
│   ├── core.py
│   ├── threading_utils.py
│   ├── banner.py
│   └── services.py
│
├── utils/
│   ├── logger.py
│   └── validators.py
│
├── config/
│   └── settings.py
│
├── scan_results.json
└── requirements.txt

