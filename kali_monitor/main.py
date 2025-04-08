import threading
import time
import os
from log_server import LogServer
from tools.ufw_monitor import UFWMonitor
from tools.nmap_monitor import NmapMonitor
from tools.tcpdump_monitor import TCPDumpMonitor
from tools.fail2ban_monitor import Fail2BanMonitor
from tools.chkrootkit_monitor import ChkrootkitMonitor
from config import LOG_DIR

def ensure_log_directory():
    """Ensure the log directory exists"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        os.chmod(LOG_DIR, 0o755)

def main():
    # Ensure log directory exists
    ensure_log_directory()
    
    # Initialize log server
    log_server = LogServer()
    
    # Initialize all monitors
    monitors = [
        UFWMonitor(log_server),
        NmapMonitor(log_server),
        TCPDumpMonitor(log_server),
        Fail2BanMonitor(log_server),
        ChkrootkitMonitor(log_server)
    ]
    
    # Start each monitor in a separate thread
    threads = []
    for monitor in monitors:
        thread = threading.Thread(target=monitor.start_monitoring)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down monitoring system...")
        log_server.close()

if __name__ == "__main__":
    main() 