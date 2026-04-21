# scanner/services.py

# Common port → service name mapping with human-readable descriptions.
SERVICES = {
    20:    "FTP Data",
    21:    "FTP Control",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP (Mail Transfer)",
    53:    "DNS",
    67:    "DHCP Server",
    68:    "DHCP Client",
    69:    "TFTP",
    79:    "Finger",
    80:    "HTTP",
    88:    "Kerberos",
    110:   "POP3",
    111:   "RPC Portmapper",
    119:   "NNTP",
    123:   "NTP",
    135:   "RPC Endpoint Mapper",
    137:   "NetBIOS Name Service",
    138:   "NetBIOS Datagram",
    139:   "NetBIOS Session",
    143:   "IMAP",
    161:   "SNMP",
    162:   "SNMP Trap",
    179:   "BGP",
    194:   "IRC",
    389:   "LDAP",
    443:   "HTTPS",
    445:   "SMB (Windows File Sharing)",
    465:   "SMTPS",
    500:   "IKE / IPSec VPN",
    514:   "Syslog",
    515:   "LPD / Printer",
    587:   "SMTP Submission",
    631:   "IPP (Printing)",
    636:   "LDAPS",
    873:   "rsync",
    989:   "FTPS Data",
    990:   "FTPS Control",
    993:   "IMAPS",
    995:   "POP3S",
    1080:  "SOCKS Proxy",
    1194:  "OpenVPN",
    1433:  "MSSQL",
    1521:  "Oracle DB",
    1723:  "PPTP VPN",
    2049:  "NFS",
    2082:  "cPanel HTTP",
    2083:  "cPanel HTTPS",
    2181:  "ZooKeeper",
    3306:  "MySQL",
    3389:  "RDP (Remote Desktop)",
    4444:  "Metasploit Default",
    5432:  "PostgreSQL",
    5900:  "VNC",
    5985:  "WinRM HTTP",
    5986:  "WinRM HTTPS",
    6379:  "Redis",
    6443:  "Kubernetes API",
    8080:  "HTTP Alternate",
    8443:  "HTTPS Alternate",
    8888:  "Jupyter Notebook",
    9000:  "PHP-FPM / SonarQube",
    9090:  "Prometheus",
    9200:  "Elasticsearch HTTP",
    9300:  "Elasticsearch Transport",
    27017: "MongoDB",
    27018: "MongoDB Shard",
}


def get_service(port):
    """
    Behavior: Looks up the service name for a given port number in the SERVICES
              dictionary and returns a human-readable label.
    Parameters:
        port (int): The port number to look up.
    Returns:
        str: The service name string if the port is known, otherwise "Unknown".
    Exceptions:
        None raised.
    """
    return SERVICES.get(port, "Unknown")
