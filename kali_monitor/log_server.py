import socket
import time
import json
from config import WINDOWS_IP, LOG_SERVER_PORT

class LogServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
    def connect(self):
        try:
            self.socket.connect((WINDOWS_IP, LOG_SERVER_PORT))
            self.connected = True
            print("Connected to Windows log receiver")
        except Exception as e:
            print(f"Failed to connect to Windows: {e}")
            self.connected = False
            
    def send_log(self, tool_name, log_data, error=None):
        if not self.connected:
            self.connect()
            
        if not self.connected:
            return False
            
        try:
            message = {
                "tool": tool_name,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log": log_data,
                "error": error
            }
            
            self.socket.send(json.dumps(message).encode() + b'\n')
            return True
        except Exception as e:
            print(f"Failed to send log: {e}")
            self.connected = False
            return False
            
    def close(self):
        if self.connected:
            self.socket.close()
            self.connected = False 