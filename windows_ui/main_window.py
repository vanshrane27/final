from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTextEdit, QLabel, QApplication, QPushButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
import socket
import json
import threading
from config import LOG_SERVER_PORT, AI_ANALYSIS_INTERVAL
from ai_analyzer import AIAnalyzer

class LogReceiver(QThread):
    log_received = pyqtSignal(str, str)  # tool_name, log_data
    error_received = pyqtSignal(str, str)  # tool_name, error
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', LOG_SERVER_PORT))
        server_socket.listen(1)
        
        while self.running:
            try:
                client_socket, _ = server_socket.accept()
                while self.running:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                        
                    message = json.loads(data.decode())
                    if message.get('error'):
                        self.error_received.emit(message['tool'], message['error'])
                    else:
                        self.log_received.emit(message['tool'], message['log'])
                        
            except Exception as e:
                print(f"Error in log receiver: {e}")
                
    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyber Threat Intelligence Platform")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize AI analyzer
        self.ai_analyzer = AIAnalyzer()
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 1px solid #3d3d3d;
            }
            QLabel {
                color: #00ff00;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #00ff00;
                border: 1px solid #4d4d4d;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create two rows of four sections each
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        
        # Create text areas for each section
        self.ufw_text = self.create_section("UFW Logs", row1)
        self.nmap_text = self.create_section("Nmap Logs", row1)
        self.tcpdump_text = self.create_section("TCPDump Logs", row1)
        self.fail2ban_text = self.create_section("Fail2Ban Logs", row1)
        
        self.chkrootkit_text = self.create_section("Chkrootkit Logs", row2)
        self.alerts_text = self.create_section("Alerts", row2)
        self.ai_analysis_text = self.create_section("AI Analysis", row2)
        self.ai_solution_text = self.create_section("AI Solution", row2)
        
        # Add rows to main layout
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        
        # Add analyze button
        analyze_button = QPushButton("Analyze Logs")
        analyze_button.clicked.connect(self.analyze_logs)
        main_layout.addWidget(analyze_button)
        
        # Start log receiver
        self.log_receiver = LogReceiver()
        self.log_receiver.log_received.connect(self.handle_log)
        self.log_receiver.error_received.connect(self.handle_error)
        self.log_receiver.start()
        
        # Set up AI analysis timer
        self.analysis_timer = QTimer()
        self.analysis_timer.timeout.connect(self.analyze_logs)
        self.analysis_timer.start(AI_ANALYSIS_INTERVAL * 1000)  # Convert to milliseconds
        
    def create_section(self, title, layout):
        container = QWidget()
        vbox = QVBoxLayout(container)
        
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        vbox.addWidget(label)
        vbox.addWidget(text_edit)
        layout.addWidget(container)
        
        return text_edit
        
    def handle_log(self, tool_name, log_data):
        # Update the appropriate text area based on tool_name
        text_areas = {
            'ufw': self.ufw_text,
            'nmap': self.nmap_text,
            'tcpdump': self.tcpdump_text,
            'fail2ban': self.fail2ban_text,
            'chkrootkit': self.chkrootkit_text
        }
        
        if tool_name in text_areas:
            text_areas[tool_name].append(log_data)
            
    def handle_error(self, tool_name, error):
        self.alerts_text.append(f"Error in {tool_name}: {error}")
        
    def analyze_logs(self):
        # Collect all logs
        all_logs = {
            'ufw': self.ufw_text.toPlainText(),
            'nmap': self.nmap_text.toPlainText(),
            'tcpdump': self.tcpdump_text.toPlainText(),
            'fail2ban': self.fail2ban_text.toPlainText(),
            'chkrootkit': self.chkrootkit_text.toPlainText()
        }
        
        # Analyze each tool's logs
        for tool, logs in all_logs.items():
            if logs:  # Only analyze if there are logs
                analysis = self.ai_analyzer.analyze_logs(tool, logs)
                self.ai_analysis_text.append(f"\n{tool.upper()} Analysis:\n{analysis['analysis']}\n")
                
                if analysis['threat_detected']:
                    solution = self.ai_analyzer.get_solution(analysis['analysis'])
                    self.ai_solution_text.append(f"\n{tool.upper()} Solution:\n{solution['solution']}\n")
                    self.alerts_text.append(f"Threat detected in {tool} logs! Check AI Analysis and Solution sections.")
                    
    def closeEvent(self, event):
        self.log_receiver.stop()
        self.analysis_timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_() 