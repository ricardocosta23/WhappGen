import os
import sys
import platform
import tkinter as tk
from tkinter import messagebox
import subprocess

from step_manager import StepManager
from styles import apply_styles
from database import setup_database
from windows_helper import is_windows, setup_windows_environment

def check_windows():
    """Check if the operating system is Windows."""
    if not is_windows():
        messagebox.showerror(
            "Incompatible Operating System",
            "This application is designed to work only on Windows. Exiting..."
        )
        sys.exit(1)

def check_dependencies():
    """Check and install required dependencies."""
    try:
        # Attempt to import required modules
        try:
            import pyautogui
            import pandas
            import requests
        except ImportError as e:
            messagebox.showwarning(
                "Missing Dependencies",
                f"Some dependencies are missing: {str(e)}\n"
                "Please run install_windows.py to set up all required dependencies."
            )
            return False
            
        # Check if AutoHotkey is installed
        try:
            # Check common paths
            ahk_paths = [
                "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe",
                "C:\\Program Files (x86)\\AutoHotkey\\AutoHotkey.exe"
            ]
            
            ahk_installed = False
            for path in ahk_paths:
                if os.path.exists(path):
                    ahk_installed = True
                    break
                    
            if not ahk_installed:
                # Try to run AutoHotkey command
                subprocess.check_call(
                    ["autohotkey", "/?"], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                ahk_installed = True
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showwarning(
                "AutoHotkey Missing",
                "AutoHotkey is required for this application.\n"
                "Please run install_windows.py to install AutoHotkey."
            )
            return False
            
        return True
    except Exception as e:
        messagebox.showerror(
            "Error Checking Dependencies",
            f"An error occurred while checking dependencies: {str(e)}"
        )
        return False

def create_app_dirs():
    """Create necessary application directories."""
    app_data_dir = os.path.join(os.getenv('APPDATA'), 'WhatsAppAutomation')
    scripts_dir = os.path.join(app_data_dir, 'scripts')
    temp_dir = os.path.join(app_data_dir, 'temp')
    
    for directory in [app_data_dir, scripts_dir, temp_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    return app_data_dir, scripts_dir, temp_dir

def main():
    """Main application entry point."""
    # Check if running on Windows
    check_windows()
    
    # Check and install dependencies if needed
    if not check_dependencies():
        # Try to setup Windows environment
        try:
            if not setup_windows_environment():
                response = messagebox.askyesno(
                    "Dependencies Missing",
                    "Some required dependencies are missing. Would you like to run the installer now?"
                )
                if response:
                    # Run the installer
                    installer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_windows.py")
                    subprocess.Popen([sys.executable, installer_path])
                    sys.exit(0)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to setup environment: {str(e)}\n"
                "Please run install_windows.py manually."
            )
    
    # Create necessary directories
    app_data_dir, scripts_dir, temp_dir = create_app_dirs()
    
    # Setup database
    db_path = os.path.join(app_data_dir, 'whatsapp_automation.db')
    setup_database(db_path)
    
    # Initialize main application window
    root = tk.Tk()
    root.title("WhatsApp Messaging Automation")
    root.geometry("800x600")
    root.minsize(800, 600)
    
    # Apply styles to the application
    apply_styles(root)
    
    # Initialize the step manager
    app = StepManager(root, db_path, scripts_dir, temp_dir)
    app.pack(fill=tk.BOTH, expand=True)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
