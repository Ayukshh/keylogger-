# Keylogger

A Python keylogger for educational and testing purposes.  
Logs keystrokes locally or remotely, with optional encryption and stealth features.

## Features

- Local and remote logging
- Encrypted log files
- Stealth mode (Windows only)
- Optional persistence (Windows startup)

## Where is the log file?

- Logs are saved to a hidden file in your system's temp directory:
  - **Linux:** `/tmp/winupdate.log`
  - **Windows:** `C:\Users\<User>\AppData\Local\Temp\winupdate.log`

## How to run

1. **Install dependencies:**
   ```bash
   pip install pynput cryptography requests
   ```

2. **Run:**
   ```bash
   python keylogger.py
   ```

3. **Stop:**  
   Press `CTRL+C` in the terminal.

## Remote Logging

- Set `REMOTE_LOGGING = True` and provide a valid `REMOTE_SERVER` URL.
- Example: Use [Pipedream](https://pipedream.com) or [RequestBin](https://requestbin.com) for testing.

## Warning

For educational use only.  
Do not use for unauthorized