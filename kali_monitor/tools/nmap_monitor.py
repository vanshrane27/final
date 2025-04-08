import subprocess
import time
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NMAP_PATH, NMAP_LOG, NMAP_INTERVAL
from log_server import LogServer

class NmapMonitor:
    def __init__(self, log_server):
        self.log_server = log_server
        
    def run(self):
        try:
            # Run a basic network scan
            scan = subprocess.run([
                NMAP_PATH,
                "-sS",  # TCP SYN scan
                "-sV",  # Version detection
                "-O",   # OS detection
                "localhost"  # Scan localhost
            ], capture_output=True, text=True)
            
            if scan.returncode == 0:
                log_data = scan.stdout
                self.log_server.send_log("nmap", log_data)
            else:
                self.log_server.send_log("nmap", "", f"Nmap scan failed: {scan.stderr}")
                
        except Exception as e:
            self.log_server.send_log("nmap", "", f"Nmap monitoring error: {str(e)}")
            
    def start_monitoring(self):
        while True:
            self.run()
            time.sleep(NMAP_INTERVAL) 