# Cyber Threat Intelligence Platform

A comprehensive security monitoring platform that allows monitoring Kali Linux systems from a Windows machine.

## Features

- Real-time monitoring of security tools:
  - UFW (Uncomplicated Firewall)
  - Nmap
  - TCPDump
  - Fail2Ban
  - Chkrootkit
- Centralized log collection and display
- AI-powered threat analysis using Google Gemini
- Dark-themed Windows UI with real-time updates
- TCP-based communication between Kali Linux and Windows

## Prerequisites

### Kali Linux
- Python 3.7+
- UFW
- Nmap
- TCPDump
- Fail2Ban
- Chkrootkit

### Windows
- Python 3.7+
- PyQt5
- Google Gemini API key

## Installation

### Kali Linux
1. Install required system tools:
```bash
sudo apt-get update
sudo apt-get install ufw nmap tcpdump fail2ban chkrootkit
```

2. Install Python requirements:
```bash
pip install -r requirements.txt
```

### Windows
1. Install Python requirements:
```bash
pip install -r requirements.txt
```

## Configuration

1. Update the IP address in `kali_monitor/config.py` to match your Windows machine's IP address.
2. Set up your Google Gemini API key in the Windows UI application.

## Usage

### Kali Linux
1. Start the monitoring system:
```bash
cd kali_monitor
python main.py
```

### Windows
1. Start the UI application:
```bash
cd windows_ui
python main_window.py
```

## Security Considerations

- Ensure proper firewall rules are in place
- Use secure network connections
- Keep all tools and dependencies updated
- Regularly review and analyze logs
- Implement proper access controls

## Troubleshooting

1. If logs are not appearing in the Windows UI:
   - Check network connectivity between Kali and Windows
   - Verify IP address configuration
   - Ensure no firewall is blocking the connection

2. If tools are not working:
   - Verify tool installations
   - Check for proper permissions
   - Review error logs in the Alerts section

## License

MIT License 