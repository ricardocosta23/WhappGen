"""
WhatsApp Automation Tool - Windows Installer
This script will install all required dependencies for the WhatsApp Automation Tool.
It checks and installs:
1. Required Python modules (pyautogui, pywin32, pandas, requests, tkinter)
2. AutoHotkey (if not already installed)
"""

import os
import sys
import ctypes
import subprocess
import tempfile
import shutil
import urllib.request
import time
import platform

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with admin privileges."""
    if is_admin():
        return True
        
    print("This installer needs administrator privileges.")
    print("It will now request elevation. Please approve the UAC prompt.")
    time.sleep(1)
    
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit(0)

def is_windows():
    """Check if running on Windows."""
    return platform.system() == "Windows"

def print_header():
    """Print installer header."""
    print("="*80)
    print(" "*25 + "WhatsApp Automation Tool Installer")
    print("="*80)
    print("\nThis installer will set up all components needed for the WhatsApp Automation Tool:")
    print("  1. Required Python modules")
    print("  2. AutoHotkey (for Windows automation)")
    print("\nPlease wait while we check your system...")
    print("-"*80)

def print_step(step_number, step_name):
    """Print step information."""
    print(f"\n[{step_number}] {step_name}")
    print("-"*80)

def check_python_modules():
    """Check if required Python modules are installed."""
    print_step(1, "Checking Python modules")
    
    required_modules = {
        "pyautogui": "Mouse and keyboard control",
        "pywin32": "Windows-specific functions",
        "pandas": "Data manipulation",
        "requests": "HTTP requests",
        "tkinter": "GUI toolkit"
    }
    
    missing_modules = []
    
    for module, description in required_modules.items():
        sys.stdout.write(f"Checking for {module} ({description})... ")
        try:
            __import__(module)
            print("OK")
        except ImportError:
            print("Missing")
            missing_modules.append(module)
    
    return missing_modules

def install_python_modules(modules):
    """Install missing Python modules."""
    if not modules:
        print("All required Python modules are already installed.")
        return True
    
    print(f"\nInstalling {len(modules)} missing modules...")
    for module in modules:
        try:
            print(f"Installing {module}... ", end="")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", module],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Done")
        except subprocess.CalledProcessError:
            print("Failed")
            print(f"Error: Failed to install {module}. Please install it manually with:")
            print(f"    pip install {module}")
            return False
    
    print("All Python modules installed successfully!")
    return True

def check_autohotkey():
    """Check if AutoHotkey is installed."""
    print_step(2, "Checking for AutoHotkey")
    
    # Common paths where AutoHotkey might be installed
    ahk_paths = [
        "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe",
        "C:\\Program Files (x86)\\AutoHotkey\\AutoHotkey.exe"
    ]
    
    # Check if AutoHotkey is in PATH
    sys.stdout.write("Checking if AutoHotkey is in PATH... ")
    try:
        subprocess.check_call(
            ["autohotkey", "/?"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Not found")
    
    # Check in common installation paths
    for path in ahk_paths:
        sys.stdout.write(f"Checking for AutoHotkey at {path}... ")
        if os.path.exists(path):
            print("Found")
            return True
        print("Not found")
    
    return False

def install_autohotkey():
    """Download and install AutoHotkey."""
    print("\nAutoHotkey is not installed. Installing now...")
    
    # AutoHotkey installer URL
    ahk_url = "https://www.autohotkey.com/download/ahk-install.exe"
    
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        installer_path = os.path.join(temp_dir, "ahk-install.exe")
        
        # Download the installer
        print("Downloading AutoHotkey installer... ", end="")
        with urllib.request.urlopen(ahk_url) as response, open(installer_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Done")
        
        # Run the installer silently
        print("Installing AutoHotkey (this may take a moment)... ", end="")
        subprocess.check_call([installer_path, "/S"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        print("Done")
        
        # Clean up
        try:
            os.unlink(installer_path)
            os.rmdir(temp_dir)
        except:
            pass
        
        return True
    except Exception as e:
        print(f"Failed\nError: {e}")
        print("\nPlease install AutoHotkey manually from: https://www.autohotkey.com/")
        return False

def create_shortcut():
    """Create a desktop shortcut for the application."""
    print_step(3, "Creating desktop shortcut")
    
    try:
        # Get paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "main.py")
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop_path, "WhatsApp Automation.lnk")
        
        # Create shortcut using PowerShell
        ps_command = f"""
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{sys.executable}"
        $Shortcut.Arguments = "{main_script}"
        $Shortcut.WorkingDirectory = "{script_dir}"
        $Shortcut.IconLocation = "{sys.executable}"
        $Shortcut.Description = "WhatsApp Automation Tool"
        $Shortcut.Save()
        """
        
        # Write the PowerShell command to a temporary file
        ps_file = os.path.join(tempfile.gettempdir(), "create_shortcut.ps1")
        with open(ps_file, "w") as f:
            f.write(ps_command)
        
        # Execute the PowerShell script
        print("Creating desktop shortcut... ", end="")
        subprocess.check_call(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Done")
        
        # Clean up
        try:
            os.unlink(ps_file)
        except:
            pass
        
        return True
    except Exception as e:
        print(f"Failed\nError: {e}")
        print("\nYou can start the application manually by running: python main.py")
        return False

def main():
    if not is_windows():
        print("Error: This installer is designed for Windows only.")
        print("The WhatsApp Automation Tool requires Windows to function.")
        input("\nPress Enter to exit...")
        return
    
    if not is_admin():
        run_as_admin()
        return
    
    print_header()
    
    # Check and install Python modules
    missing_modules = check_python_modules()
    if not install_python_modules(missing_modules):
        print("\nWarning: Some Python modules could not be installed.")
        print("The application may not function correctly.")
    
    # Check and install AutoHotkey
    if not check_autohotkey():
        if not install_autohotkey():
            print("\nWarning: AutoHotkey could not be installed.")
            print("The application will not be able to send automated messages.")
    
    # Create shortcut
    create_shortcut()
    
    print("\n" + "="*80)
    print(" "*20 + "Installation Complete!")
    print("="*80)
    print("\nThe WhatsApp Automation Tool has been installed successfully.")
    print("You can now start the application from the desktop shortcut.")
    
    input("\nPress Enter to exit the installer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
        input("\nPress Enter to exit...")