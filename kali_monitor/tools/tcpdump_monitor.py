import subprocess
import time
import threading
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TCPDUMP_PATH, TCPDUMP_LOG, TCPDUMP_INTERVAL
from log_server import LogServer

class TCPDumpMonitor:
    def __init__(self, log_server):
        self.log_server = log_server
        self.process = None
        self.running = False
        
    def run(self):
        try:
            # Start TCPDump in a separate thread
            self.running = True
            self.process = subprocess.Popen(
                [
                    TCPDUMP_PATH,
                    "-i", "any",  # Monitor all interfaces
                    "-n",  # Don't resolve hostnames
                    "-l",  # Line buffered output
                    "-q",  # Quick output
                    "port not 22"  # Exclude SSH traffic
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Read output in a separate thread
            threading.Thread(target=self._read_output, daemon=True).start()
            
        except Exception as e:
            self.log_server.send_log("tcpdump", "", f"TCPDump monitoring error: {str(e)}")
            
    def _read_output(self):
        while self.running and self.process:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.log_server.send_log("tcpdump", line.strip())
                else:
                    break
            except Exception as e:
                self.log_server.send_log("tcpdump", "", f"Error reading TCPDump output: {str(e)}")
                break
                
    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                
    def start_monitoring(self):
        while True:
            self.run()
            time.sleep(TCPDUMP_INTERVAL)
            self.stop() 