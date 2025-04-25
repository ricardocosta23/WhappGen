import os
import webbrowser
import subprocess

class WhatsAppHelper:
    def __init__(self):
        self.whatsapp_notified = False
    
    def is_whatsapp_installed(self):
        """Check if WhatsApp Desktop is installed."""
        # Common installation paths for WhatsApp Desktop
        possible_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'WhatsApp', 'WhatsApp.exe'),
            os.path.join(os.getenv('PROGRAMFILES'), 'WhatsApp', 'WhatsApp.exe'),
            os.path.join(os.getenv('PROGRAMFILES(X86)'), 'WhatsApp', 'WhatsApp.exe')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return True
        return False
    
    def open_whatsapp(self):
        """Open WhatsApp Desktop application or web version."""
        try:
            # Try to find WhatsApp Desktop in common locations
            whatsapp_paths = [
                os.path.join(os.getenv('LOCALAPPDATA'), 'WhatsApp', 'WhatsApp.exe'),
                os.path.join(os.getenv('PROGRAMFILES'), 'WhatsApp', 'WhatsApp.exe'),
                os.path.join(os.getenv('PROGRAMFILES(X86)'), 'WhatsApp', 'WhatsApp.exe')
            ]
            
            for path in whatsapp_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return True
            
            # If WhatsApp Desktop not found, open the web version
            webbrowser.open("https://web.whatsapp.com/")
            return True
        except Exception as e:
            return False
    
    def is_whatsapp_notified(self):
        """Check if the user has been notified about WhatsApp Desktop."""
        return self.whatsapp_notified
    
    def set_whatsapp_notified(self, value):
        """Set the notification status for WhatsApp Desktop."""
        self.whatsapp_notified = value
