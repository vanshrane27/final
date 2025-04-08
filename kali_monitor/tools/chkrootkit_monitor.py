import subprocess
import time
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHKROOTKIT_PATH, CHKROOTKIT_LOG, CHKROOTKIT_INTERVAL
from log_server import LogServer

class ChkrootkitMonitor:
    def __init__(self, log_server):
        self.log_server = log_server
        
    def run(self):
        try:
            # Run chkrootkit with quiet mode
            result = subprocess.run(
                [CHKROOTKIT_PATH, "-q"],  # Quiet mode
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Check if there are any suspicious findings
                if "INFECTED" in result.stdout or "Warning" in result.stdout:
                    self.log_server.send_log("chkrootkit", result.stdout)
                    # Send an alert for suspicious findings
                    self.log_server.send_log("alerts", f"Chkrootkit found suspicious files:\n{result.stdout}")
                else:
                    self.log_server.send_log("chkrootkit", "No suspicious files found")
            else:
                self.log_server.send_log("chkrootkit", "", f"Chkrootkit scan failed: {result.stderr}")
                
        except Exception as e:
            self.log_server.send_log("chkrootkit", "", f"Chkrootkit monitoring error: {str(e)}")
            
    def start_monitoring(self):
        while True:
            self.run()
            time.sleep(CHKROOTKIT_INTERVAL) 