import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import webbrowser
import os
import subprocess
import pyautogui
import pandas as pd

from database import save_security_number

class SetupFrame(ttk.Frame):
    def __init__(self, parent, ahk_manager, whatsapp_helper, status_callback):
        super().__init__(parent)
        self.parent = parent
        self.ahk_manager = ahk_manager
        self.whatsapp_helper = whatsapp_helper
        self.status_callback = status_callback
        
        self.create_widgets()
        self.check_dependencies()
    
    def create_widgets(self):
        """Create widgets for the setup frame."""
        # Title
        title = ttk.Label(
            self, 
            text="Step 1 - Setup Dependencies", 
            font=("Arial", 14, "bold")
        )
        title.pack(pady=(0, 20))
        
        # AutoHotkey section
        ahk_frame = ttk.LabelFrame(self, text="AutoHotkey Installation")
        ahk_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ahk_status = ttk.Label(ahk_frame, text="Checking...", foreground="blue")
        self.ahk_status.pack(fill=tk.X, padx=10, pady=5)
        
        self.ahk_button = ttk.Button(
            ahk_frame, 
            text="Install AutoHotkey", 
            command=self.install_autohotkey
        )
        self.ahk_button.pack(padx=10, pady=5)
        
        # WhatsApp Desktop section
        whatsapp_frame = ttk.LabelFrame(self, text="WhatsApp Desktop Installation")
        whatsapp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.whatsapp_status = ttk.Label(whatsapp_frame, text="Checking...", foreground="blue")
        self.whatsapp_status.pack(fill=tk.X, padx=10, pady=5)
        
        self.whatsapp_button = ttk.Button(
            whatsapp_frame, 
            text="Download WhatsApp Desktop", 
            command=self.download_whatsapp
        )
        self.whatsapp_button.pack(padx=10, pady=5)
        
        # Status message
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Checking dependencies...", 
            foreground="blue",
            wraplength=450
        )
        self.status_label.pack(fill=tk.X)
    
    def check_dependencies(self):
        """Check for required dependencies."""
        threading.Thread(target=self._check_dependencies).start()
    
    def _check_dependencies(self):
        """Background thread for checking dependencies."""
        # Check AutoHotkey
        if self.ahk_manager.is_autohotkey_installed():
            self.ahk_status.config(
                text="✓ AutoHotkey is installed", 
                foreground="green"
            )
            self.ahk_button.config(state=tk.DISABLED)
        else:
            self.ahk_status.config(
                text="✗ AutoHotkey is not installed", 
                foreground="red"
            )
            self.ahk_button.config(state=tk.NORMAL)
        
        # Check WhatsApp Desktop
        if self.ahk_manager.is_whatsapp_desktop_installed():
            self.whatsapp_status.config(
                text="✓ WhatsApp Desktop is installed", 
                foreground="green"
            )
            self.whatsapp_button.config(state=tk.DISABLED)
            self.whatsapp_helper.set_whatsapp_notified(True)
        else:
            self.whatsapp_status.config(
                text="✗ WhatsApp Desktop is not installed", 
                foreground="red"
            )
            self.whatsapp_button.config(state=tk.NORMAL)
        
        self.update_status("Dependencies check completed.")
    
    def install_autohotkey(self):
        """Install AutoHotkey silently."""
        self.update_status("Installing AutoHotkey...")
        self.ahk_button.config(state=tk.DISABLED)
        
        threading.Thread(target=self._install_autohotkey).start()
    
    def _install_autohotkey(self):
        """Background thread for installing AutoHotkey."""
        success, message = self.ahk_manager.install_autohotkey(self.update_status)
        
        if success:
            self.ahk_status.config(
                text="✓ AutoHotkey is installed", 
                foreground="green"
            )
            self.ahk_button.config(state=tk.DISABLED)
        else:
            self.ahk_status.config(
                text="✗ AutoHotkey installation failed", 
                foreground="red"
            )
            self.ahk_button.config(state=tk.NORMAL)
            messagebox.showerror("Installation Error", message)
        
        self.update_status(message)
    
    def download_whatsapp(self):
        """Open the WhatsApp Desktop download page."""
        webbrowser.open("https://www.whatsapp.com/download")
        self.update_status("WhatsApp Desktop download page opened in browser.")
        self.whatsapp_helper.set_whatsapp_notified(True)
    
    def update_status(self, message):
        """Update the status message."""
        self.status_label.config(text=message)
        if self.status_callback:
            self.status_callback(message)

class CoordinatesFrame(ttk.Frame):
    def __init__(self, parent, db_path, whatsapp_helper, capture_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_path = db_path
        self.whatsapp_helper = whatsapp_helper
        self.capture_callback = capture_callback
        self.overlay_active = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create widgets for the coordinates frame."""
        # Title
        title = ttk.Label(
            self, 
            text="Step 2 - Capture WhatsApp Message Field Coordinates", 
            font=("Arial", 14, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self, text="Instructions")
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = (
            "1. Click the 'Open WhatsApp' button to launch WhatsApp Desktop.\n"
            "2. Click the 'Start Capture' button to begin the coordinates capture process.\n"
            "3. A cross-hair will appear. Move it to the WhatsApp message input field.\n"
            "4. Press 'OK' to capture the coordinates.\n\n"
            "These coordinates will be used to automate clicking on the message field."
        )
        
        instructions = ttk.Label(
            instructions_frame, 
            text=instructions_text, 
            wraplength=550, 
            justify=tk.LEFT
        )
        instructions.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.open_whatsapp_btn = ttk.Button(
            buttons_frame, 
            text="Open WhatsApp", 
            command=self.open_whatsapp
        )
        self.open_whatsapp_btn.pack(side=tk.LEFT, padx=5)
        
        self.start_capture_btn = ttk.Button(
            buttons_frame, 
            text="Start Capture", 
            command=self.start_capture
        )
        self.start_capture_btn.pack(side=tk.LEFT, padx=5)
        
        # Status message
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Waiting to capture coordinates...", 
            foreground="blue",
            wraplength=450
        )
        self.status_label.pack(fill=tk.X)
        
        # Coordinates display
        self.coords_frame = ttk.LabelFrame(self, text="Captured Coordinates")
        self.coords_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.coords_label = ttk.Label(
            self.coords_frame, 
            text="No coordinates captured yet", 
            foreground="gray"
        )
        self.coords_label.pack(fill=tk.X, padx=10, pady=10)
    
    def open_whatsapp(self):
        """Open WhatsApp Desktop application."""
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
                    self.status_label.config(text="WhatsApp Desktop opened.")
                    return
            
            # If WhatsApp Desktop not found, open the web version
            webbrowser.open("https://web.whatsapp.com/")
            self.status_label.config(text="WhatsApp Web opened in browser.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open WhatsApp: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")
    
    def start_capture(self):
        """Start the coordinates capture process."""
        if self.overlay_active:
            messagebox.showinfo("Capture in Progress", "Coordinate capture is already active.")
            return
            
        self.overlay_active = True
        self.status_label.config(text="Move cursor to WhatsApp message field and click to capture coordinates.")
        
        # Create a simple overlay
        overlay = tk.Toplevel(self)
        overlay.title("Capture Coordinates")
        overlay.attributes("-topmost", True)
        overlay.geometry("300x150")
        overlay.resizable(False, False)
        
        ttk.Label(
            overlay, 
            text="Position your cursor over the\nWhatsApp message field",
            font=("Arial", 12),
            justify=tk.CENTER
        ).pack(pady=10)
        
        capture_btn = ttk.Button(
            overlay, 
            text="Capture Coordinates",
            command=lambda: self.do_capture(overlay)
        )
        capture_btn.pack(pady=10)
        
        cancel_btn = ttk.Button(
            overlay, 
            text="Cancel",
            command=lambda: self.cancel_capture(overlay)
        )
        cancel_btn.pack(pady=5)
    
    def do_capture(self, overlay):
        """Capture the current cursor coordinates."""
        x, y = pyautogui.position()
        overlay.destroy()
        
        self.status_label.config(text=f"Coordinates captured: X={x}, Y={y}")
        self.coords_label.config(
            text=f"X: {x}, Y: {y}", 
            foreground="green"
        )
        
        if self.capture_callback:
            self.capture_callback(x, y)
            
        self.overlay_active = False
    
    def cancel_capture(self, overlay):
        """Cancel the coordinate capture process."""
        overlay.destroy()
        self.status_label.config(text="Coordinate capture cancelled.")
        self.overlay_active = False

class SecurityNumberFrame(ttk.Frame):
    def __init__(self, parent, db_path, current_value=""):
        super().__init__(parent)
        self.parent = parent
        self.db_path = db_path
        self.current_value = current_value
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create widgets for the security number frame."""
        # Title
        title = ttk.Label(
            self, 
            text="Step 3 - Enter Security Number", 
            font=("Arial", 14, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self, text="Instructions")
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = (
            "Enter your security number below. This number will be used when connecting to WhatsApp.\n\n"
            "The security number should be in the format of a valid phone number with country code, "
            "without any spaces or special characters (e.g., 551234567890)."
        )
        
        instructions = ttk.Label(
            instructions_frame, 
            text=instructions_text, 
            wraplength=550, 
            justify=tk.LEFT
        )
        instructions.pack(fill=tk.X, padx=10, pady=10)
        
        # Security number input
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Label(
            input_frame, 
            text="Security Number:", 
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        self.security_number = ttk.Entry(input_frame, width=20)
        self.security_number.pack(side=tk.LEFT, padx=5)
        
        # Populate with current value if available
        if self.current_value:
            self.security_number.insert(0, self.current_value)
        
        # Save button
        self.save_btn = ttk.Button(
            input_frame, 
            text="Save", 
            command=self.save_security_number
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Status message
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Enter your security number", 
            foreground="blue",
            wraplength=450
        )
        self.status_label.pack(fill=tk.X)
    
    def save_security_number(self):
        """Save the security number to the database."""
        security_number = self.security_number.get().strip()
        
        if not security_number:
            messagebox.showerror("Error", "Please enter a security number.")
            return
        
        # Validate security number format (basic check)
        if not security_number.isdigit():
            messagebox.showerror(
                "Invalid Format", 
                "Security number should contain only digits."
            )
            return
        
        save_security_number(self.db_path, security_number)
        
        self.status_label.config(
            text="Security number saved successfully.", 
            foreground="green"
        )
    
    def get_security_number(self):
        """Get the current security number from the input field."""
        return self.security_number.get().strip()

class MessageFieldsFrame(ttk.Frame):
    def __init__(self, parent, db_path, messages, process_csv_callback, generate_script_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_path = db_path
        self.messages = messages  # Dictionary to store message values
        self.process_csv_callback = process_csv_callback
        self.generate_script_callback = generate_script_callback
        
        self.create_widgets()
        self.load_messages()
    
    def create_widgets(self):
        """Create widgets for the message fields frame."""
        # Title
        title = ttk.Label(
            self, 
            text="Step 4 - Configure Messages", 
            font=("Arial", 14, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self, text="Instructions")
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = (
            "1. Enter the messages you want to send in the fields below.\n"
            "2. Upload a CSV file with phone numbers in the 'Numero de Telefone' column.\n"
            "3. Click 'Generate Script' to create the AutoHotkey script.\n\n"
            "The script will cycle through the message sets (A, B, C, D) for each phone number."
        )
        
        instructions = ttk.Label(
            instructions_frame, 
            text=instructions_text, 
            wraplength=550, 
            justify=tk.LEFT
        )
        instructions.pack(fill=tk.X, padx=10, pady=10)
        
        # Message fields container with scrollbar
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Message fields
        self.message_entries = {}
        
        # Create a frame for each column
        columns = ['A', 'B', 'C', 'D']
        column_frames = {}
        
        # Create the column headers
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        # Add padding frame for row numbers
        ttk.Label(header_frame, text="", width=3).pack(side=tk.LEFT, padx=5)
        
        for col in columns:
            ttk.Label(
                header_frame, 
                text=f"Column {col}", 
                font=("Arial", 10, "bold"), 
                width=25,
                anchor="center"
            ).pack(side=tk.LEFT, padx=5)
        
        # Create rows of message fields
        for row in range(1, 5):  # 4 rows
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            # Row number
            ttk.Label(
                row_frame, 
                text=f"{row}:", 
                width=3,
                font=("Arial", 10, "bold")
            ).pack(side=tk.LEFT, padx=5)
            
            for col in columns:
                field_frame = ttk.Frame(row_frame)
                field_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                
                msg_key = f"msg{row}{col}"
                entry = tk.Text(field_frame, height=3, width=25)
                entry.pack(fill=tk.BOTH, expand=True)
                
                self.message_entries[msg_key] = entry
        
        # CSV upload and script generation
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.upload_csv_btn = ttk.Button(
            buttons_frame, 
            text="Upload CSV", 
            command=self.upload_csv
        )
        self.upload_csv_btn.pack(side=tk.LEFT, padx=5)
        
        self.generate_script_btn = ttk.Button(
            buttons_frame, 
            text="Generate Script", 
            command=self.generate_script
        )
        self.generate_script_btn.pack(side=tk.LEFT, padx=5)
        
        # Status message
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Enter your messages and upload a CSV file with phone numbers.", 
            foreground="blue",
            wraplength=550
        )
        self.status_label.pack(fill=tk.X)
    
    def load_messages(self):
        """Load previously entered messages if available."""
        for key, entry in self.message_entries.items():
            if key in self.messages:
                entry.delete("1.0", tk.END)
                entry.insert("1.0", self.messages[key])
    
    def get_messages(self):
        """Get all message values from the entry fields."""
        messages = {}
        for key, entry in self.message_entries.items():
            messages[key] = entry.get("1.0", "end-1c")
        return messages
    
    def upload_csv(self):
        """Open a file dialog to select a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            # Process the CSV file
            if self.process_csv_callback:
                success = self.process_csv_callback(file_path)
                if success:
                    self.status_label.config(
                        text=f"CSV file '{os.path.basename(file_path)}' processed successfully.", 
                        foreground="green"
                    )
                else:
                    self.status_label.config(
                        text="Error processing CSV file. See error message for details.", 
                        foreground="red"
                    )
    
    def generate_script(self):
        """Generate the AutoHotkey script."""
        # First, save all message fields
        self.messages = self.get_messages()
        
        # Then, generate the script
        if self.generate_script_callback:
            success = self.generate_script_callback()
            if success:
                self.status_label.config(
                    text="Script generated successfully. Proceed to the next step to run it.", 
                    foreground="green"
                )
            else:
                self.status_label.config(
                    text="Error generating script. See error message for details.", 
                    foreground="red"
                )

class RunScriptFrame(ttk.Frame):
    def __init__(self, parent, ahk_manager, run_script_callback):
        super().__init__(parent)
        self.parent = parent
        self.ahk_manager = ahk_manager
        self.run_script_callback = run_script_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create widgets for the run script frame."""
        # Title
        title = ttk.Label(
            self, 
            text="Step 5 - Run Automation", 
            font=("Arial", 14, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self, text="Instructions")
        instructions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        instructions_text = (
            "1. Make sure WhatsApp Desktop is open and you are logged in.\n"
            "2. Click the 'Run Automation' button to start the process.\n"
            "3. Do not touch your keyboard or mouse during the automation.\n"
            "4. The script will automatically navigate through WhatsApp and send messages.\n\n"
            "IMPORTANT: To stop the automation at any time, press Alt+Esc."
        )
        
        instructions = ttk.Label(
            instructions_frame, 
            text=instructions_text, 
            wraplength=550, 
            justify=tk.LEFT
        )
        instructions.pack(fill=tk.X, padx=10, pady=10)
        
        # Warning
        warning_frame = ttk.LabelFrame(self, text="Warning")
        warning_frame.pack(fill=tk.X, padx=10, pady=10)
        
        warning_text = (
            "This automation will take control of your mouse and keyboard. "
            "Do not interact with your computer until the process is complete. "
            "The application will attempt to send messages to all numbers in your CSV file."
        )
        
        warning = ttk.Label(
            warning_frame, 
            text=warning_text, 
            wraplength=550, 
            justify=tk.LEFT,
            foreground="red"
        )
        warning.pack(fill=tk.X, padx=10, pady=10)
        
        # Run button
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.run_btn = ttk.Button(
            buttons_frame, 
            text="Run Automation", 
            command=self.run_script,
            style="Accent.TButton"
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.exit_btn = ttk.Button(
            buttons_frame, 
            text="Exit Application", 
            command=self.exit_application
        )
        self.exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Status message
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Ready to run automation. Click the 'Run Automation' button to begin.", 
            foreground="blue",
            wraplength=550
        )
        self.status_label.pack(fill=tk.X)
    
    def run_script(self):
        """Run the AutoHotkey script."""
        # Confirm with the user
        result = messagebox.askyesno(
            "Confirm Automation", 
            "The automation will take control of your mouse and keyboard. "
            "Make sure WhatsApp Desktop is open and you are ready. Continue?"
        )
        
        if not result:
            return
            
        # Disable the run button to prevent multiple executions
        self.run_btn.config(state=tk.DISABLED)
        
        # Run the script
        if self.run_script_callback:
            success = self.run_script_callback()
            if success:
                self.status_label.config(
                    text="Automation is running. Please do not interfere with your computer.", 
                    foreground="green"
                )
            else:
                self.status_label.config(
                    text="Error running automation. See error message for details.", 
                    foreground="red"
                )
                self.run_btn.config(state=tk.NORMAL)
    
    def exit_application(self):
        """Exit the application."""
        result = messagebox.askyesno(
            "Exit Application", 
            "Are you sure you want to exit the application?"
        )
        
        if result:
            self.parent.winfo_toplevel().destroy()
    
    def update_status(self, message):
        """Update the status message."""
        self.status_label.config(text=message)
