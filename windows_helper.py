import os
import sys
import subprocess
import ctypes
import tempfile
import urllib.request
import shutil
import platform



def create_wgen_folder():
    """Create Wgen folder in temp directory if it doesn't exist."""
    try:
        temp_dir = os.path.join(tempfile.gettempdir(), "Wgen")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir
    except Exception as e:
        print(f"Error creating Wgen folder: {e}")
        return None


def is_admin():
    """Check if the script is running with admin privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with admin privileges."""
    if is_admin():
        return True
        
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    return False

def is_windows():
    """Check if the current OS is Windows."""
    return platform.system() == "Windows"

def check_python_modules(required_modules):
    """Check if required Python modules are installed."""
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    return missing_modules

def install_modules(modules):
    """Install Python modules using pip."""
    for module in modules:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Successfully installed {module}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {module}")
            return False
    return True

def check_autohotkey():
    """Check if AutoHotkey is installed."""
    try:
        # Try to find AutoHotkey executable
        autohotkey_paths = [
            "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe",
            "C:\\Program Files (x86)\\AutoHotkey\\AutoHotkey.exe",
        ]
        
        for path in autohotkey_paths:
            if os.path.exists(path):
                return True
                
        # Try to run the autohotkey command
        subprocess.check_call(["autohotkey", "/?"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_file(url, target_path):
    """Download a file from a URL to a target path."""
    try:
        with urllib.request.urlopen(url) as response, open(target_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def install_autohotkey():
    """Download and install AutoHotkey."""
    try:
        # AutoHotkey installer URL
        ahk_url = "https://www.autohotkey.com/download/ahk-install.exe"
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        installer_path = os.path.join(temp_dir, "ahk-install.exe")
        
        # Download the installer
        print("Downloading AutoHotkey installer...")
        if not download_file(ahk_url, installer_path):
            return False
        
        # Run the installer silently
        print("Installing AutoHotkey...")
        subprocess.check_call([installer_path, "/S"])
        
        # Clean up
        os.unlink(installer_path)
        os.rmdir(temp_dir)
        
        print("AutoHotkey installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing AutoHotkey: {e}")
        return False

def setup_windows_environment():
    """Set up the Windows environment for WhatsApp automation."""
    if not is_windows():
        print("This script is designed to run on Windows only.")
        return False
    
    # Required Python modules
    required_modules = ["pyautogui", "pywin32", "pandas", "requests", "tkinter"]
    
    # Check if running as admin
    if not is_admin():
        print("This script requires admin privileges. Restarting with admin rights...")
        return run_as_admin()
    
    # Check for required Python modules
    missing_modules = check_python_modules(required_modules)
    if missing_modules:
        print(f"Missing required Python modules: {', '.join(missing_modules)}")
        print("Installing missing modules...")
        install_modules(missing_modules)
    
    # Check for AutoHotkey
    if not check_autohotkey():
        print("AutoHotkey is not installed. Installing AutoHotkey...")
        if not install_autohotkey():
            print("Failed to install AutoHotkey. Please install it manually.")
            return False
    
    print("All dependencies are installed and ready!")
    return True

if __name__ == "__main__":
    if is_windows():
        setup_windows_environment()
    else:
        print("This is not a Windows system. The WhatsApp automation tool requires Windows.")