import subprocess
import time
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FAIL2BAN_PATH, FAIL2BAN_LOG, FAIL2BAN_INTERVAL
from log_server import LogServer

class Fail2BanMonitor:
    def __init__(self, log_server):
        self.log_server = log_server
        
    def run(self):
        try:
            # Get Fail2Ban status
            status = subprocess.run([FAIL2BAN_PATH, "status"], capture_output=True, text=True)
            if status.returncode == 0:
                self.log_server.send_log("fail2ban", status.stdout)
            else:
                self.log_server.send_log("fail2ban", "", f"Fail2Ban status command failed: {status.stderr}")
                
            # Get detailed jail status
            jails = subprocess.run([FAIL2BAN_PATH, "status", "jail"], capture_output=True, text=True)
            if jails.returncode == 0:
                self.log_server.send_log("fail2ban", jails.stdout)
            else:
                self.log_server.send_log("fail2ban", "", f"Fail2Ban jail status command failed: {jails.stderr}")
                
            # Get banned IPs
            for jail in ["sshd", "apache", "nginx"]:  # Common jails
                banned = subprocess.run([FAIL2BAN_PATH, "status", jail], capture_output=True, text=True)
                if banned.returncode == 0:
                    self.log_server.send_log("fail2ban", f"\n{jail} jail status:\n{banned.stdout}")
                    
        except Exception as e:
            self.log_server.send_log("fail2ban", "", f"Fail2Ban monitoring error: {str(e)}")
            
    def start_monitoring(self):
        while True:
            self.run()
            time.sleep(FAIL2BAN_INTERVAL) 