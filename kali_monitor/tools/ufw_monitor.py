import subprocess
import time
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import UFW_PATH, UFW_LOG, UFW_INTERVAL
from log_server import LogServer

class UFWMonitor:
    def __init__(self, log_server):
        self.log_server = log_server
        
    def run(self):
        try:
            # Get UFW status
            status = subprocess.run([UFW_PATH, "status"], capture_output=True, text=True)
            if status.returncode == 0:
                log_data = status.stdout
                self.log_server.send_log("ufw", log_data)
            else:
                self.log_server.send_log("ufw", "", f"UFW status command failed: {status.stderr}")
                
            # Get UFW logs
            logs = subprocess.run([UFW_PATH, "status", "verbose"], capture_output=True, text=True)
            if logs.returncode == 0:
                log_data = logs.stdout
                self.log_server.send_log("ufw", log_data)
            else:
                self.log_server.send_log("ufw", "", f"UFW verbose status command failed: {logs.stderr}")
                
        except Exception as e:
            self.log_server.send_log("ufw", "", f"UFW monitoring error: {str(e)}")
            
    def start_monitoring(self):
        while True:
            self.run()
            time.sleep(UFW_INTERVAL) 