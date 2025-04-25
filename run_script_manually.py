#!/usr/bin/env python3
"""
WhatsApp Automation Script Runner
This script runs a generated AutoHotkey script for WhatsApp automation.
It requires AutoHotkey to be installed on Windows.
"""

import os
import sys
import subprocess
import time
import platform
import tkinter as tk
from tkinter import filedialog, messagebox

class ScriptRunner:
    def __init__(self):
        self.ahk_exe_path = None
        self.script_path = None
        
    def check_platform(self):
        """Check if running on Windows."""
        if platform.system() != "Windows":
            print("Error: This script can only run on Windows.")
            return False
        return True
        
    def find_autohotkey(self):
        """Find AutoHotkey executable."""
        # Common installation paths for AutoHotkey
        possible_paths = [
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.ahk_exe_path = path
                return True
                
        # Check if it's in PATH
        try:
            result = subprocess.run(['where', 'AutoHotkey.exe'], 
                                 capture_output=True, 
                                 text=True, 
                                 check=False)
            if result.returncode == 0:
                self.ahk_exe_path = result.stdout.strip().split('\n')[0]
                return True
        except:
            pass
            
        return False
    
    def download_autohotkey(self):
        """Prompt to download AutoHotkey."""
        if messagebox.askyesno("AutoHotkey Not Found", 
                            "AutoHotkey is required to run the script but was not found. Would you like to open the AutoHotkey download page?"):
            os.system("start https://www.autohotkey.com/download/")
            
    def select_script(self):
        """Open file dialog to select the script."""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        script_path = filedialog.askopenfilename(
            title="Select AutoHotkey Script",
            filetypes=[("AutoHotkey Scripts", "*.ahk"), ("All Files", "*.*")]
        )
        
        if script_path and os.path.exists(script_path):
            self.script_path = script_path
            return True
            
        return False
    
    def run_script(self):
        """Run the selected script with AutoHotkey."""
        try:
            # Run the script using AutoHotkey
            if not self.ahk_exe_path or not self.script_path:
                print("Error: AutoHotkey or script path not set.")
                return False
                
            print(f"Running script: {self.script_path}")
            print("Please do not interfere with the automation.")
            print("Press Ctrl+C to stop the script.")
            
            # Run the script
            subprocess.Popen([self.ahk_exe_path, self.script_path])
            
            return True
        except Exception as e:
            print(f"Error running script: {str(e)}")
            return False
    
    def run(self):
        """Main execution flow."""
        # Check if running on Windows
        if not self.check_platform():
            input("\nPress Enter to exit...")
            return False
            
        # Find AutoHotkey executable
        print("Checking for AutoHotkey installation...")
        if not self.find_autohotkey():
            print("AutoHotkey not found.")
            self.download_autohotkey()
            input("\nPlease install AutoHotkey and run this script again. Press Enter to exit...")
            return False
            
        print(f"AutoHotkey found at: {self.ahk_exe_path}")
        
        # Select script
        print("Please select the AutoHotkey script file (.ahk)...")
        if not self.select_script():
            print("No script selected.")
            input("\nPress Enter to exit...")
            return False
            
        # Run the script
        if self.run_script():
            print("Script started successfully.")
            input("\nPress Enter to exit this window (the script will continue running)...")
            return True
        else:
            print("Failed to run script.")
            input("\nPress Enter to exit...")
            return False

if __name__ == "__main__":
    try:
        runner = ScriptRunner()
        runner.run()
    except KeyboardInterrupt:
        print("\n\nScript execution cancelled by user.")
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
        input("\nPress Enter to exit...")