import os

# Log file paths
LOG_DIR = "/var/log/cyber_monitor"
UFW_LOG = os.path.join(LOG_DIR, "ufw.log")
NMAP_LOG = os.path.join(LOG_DIR, "nmap.log")
TCPDUMP_LOG = os.path.join(LOG_DIR, "tcpdump.log")
FAIL2BAN_LOG = os.path.join(LOG_DIR, "fail2ban.log")
CHKROOTKIT_LOG = os.path.join(LOG_DIR, "chkrootkit.log")

# Network settings for log server
WINDOWS_IP = "192.168.0.110"  # Update this with your Windows machine's IP
LOG_SERVER_PORT = 5000

# Monitoring intervals (in seconds)
UFW_INTERVAL = 300  # 5 minutes
NMAP_INTERVAL = 3600  # 1 hour
TCPDUMP_INTERVAL = 300  # 5 minutes
FAIL2BAN_INTERVAL = 300  # 5 minutes
CHKROOTKIT_INTERVAL = 3600  # 1 hour

# Tool paths
UFW_PATH = "/usr/sbin/ufw"
NMAP_PATH = "/usr/bin/nmap"
TCPDUMP_PATH = "/usr/sbin/tcpdump"
FAIL2BAN_PATH = "/usr/bin/fail2ban-client"
CHKROOTKIT_PATH = "/usr/sbin/chkrootkit" 