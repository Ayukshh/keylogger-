# Keylogger

A Python keylogger for educational and testing purposes.  
Logs keystrokes locally or remotely, with optional encryption and stealth features.

## Features

- Local and remote logging
- Encrypted log files
- Stealth mode (Windows only)
- Optional persistence (Windows startup)

## Usage

1. **Install dependencies:**
   ```bash
   pip install pynput cryptography requests
   ```

2. **Run the keylogger:**
   ```bash
   python keylogger.py
   ```

3. **Stop:**  
   Press `CTRL+C` in the terminal.

## Configuration

Edit the top of `keylogger.py` to enable/disable features:
- `STEALTH_MODE`
- `PERSISTENCE`
- `LOCAL_LOGGING`
- `REMOTE_LOGGING`
- `ENCRYPT_LOGS`
- `REMOTE_SERVER` (for remote logging)

## Disclaimer

This project is for educational use only.  
Do not use it