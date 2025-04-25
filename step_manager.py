import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import pandas as pd
import os
import threading
import time
import webbrowser

from ui_components import (
    SetupFrame, CoordinatesFrame, SecurityNumberFrame, 
    MessageFieldsFrame, RunScriptFrame
)
from autohotkey_manager import AutoHotkeyManager
from database import (
    save_coordinates, save_security_number, 
    get_settings, process_csv_file, get_all_phone_numbers
)
from whatsapp_helper import WhatsAppHelper

class StepManager(ttk.Frame):
    def __init__(self, parent, db_path, scripts_dir, temp_dir):
        super().__init__(parent)
        self.parent = parent
        self.db_path = db_path
        self.scripts_dir = scripts_dir
        self.temp_dir = temp_dir
        
        self.current_step = 1
        self.total_steps = 5
        
        # Initialize managers
        self.ahk_manager = AutoHotkeyManager(scripts_dir, temp_dir)
        self.whatsapp_helper = WhatsAppHelper()
        
        # Message storage dictionary
        self.messages = {}
        
        self.create_widgets()
        self.load_frame(self.current_step)
    
    def create_widgets(self):
        """Create the main application widgets."""
        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with step indicator
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Step indicator
        self.step_indicator = ttk.Label(
            self.header_frame, 
            text=f"Step {self.current_step} of {self.total_steps}", 
            font=("Arial", 12, "bold")
        )
        self.step_indicator.pack(side=tk.LEFT)
        
        # Content frame (will hold the step-specific frames)
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Navigation buttons
        self.nav_frame = ttk.Frame(self.main_container)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.prev_button = ttk.Button(
            self.nav_frame, 
            text="Previous", 
            command=self.go_previous,
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = ttk.Button(
            self.nav_frame, 
            text="Next", 
            command=self.go_next
        )
        self.next_button.pack(side=tk.RIGHT)
    
    def load_frame(self, step):
        """Load the appropriate frame for the current step."""
        # Clear the current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update step indicator
        self.step_indicator.config(text=f"Step {step} of {self.total_steps}")
        
        # Enable/disable navigation buttons
        self.prev_button.config(state=tk.NORMAL if step > 1 else tk.DISABLED)
        
        # Load the appropriate frame
        if step == 1:
            SetupFrame(
                self.content_frame, 
                self.ahk_manager, 
                self.whatsapp_helper, 
                self.update_status
            ).pack(fill=tk.BOTH, expand=True)
        elif step == 2:
            CoordinatesFrame(
                self.content_frame, 
                self.db_path, 
                self.whatsapp_helper, 
                self.capture_coordinates
            ).pack(fill=tk.BOTH, expand=True)
        elif step == 3:
            settings = get_settings(self.db_path)
            SecurityNumberFrame(
                self.content_frame, 
                self.db_path, 
                settings.get('security_number', '') if settings else ''
            ).pack(fill=tk.BOTH, expand=True)
        elif step == 4:
            MessageFieldsFrame(
                self.content_frame, 
                self.db_path, 
                self.messages, 
                self.process_csv, 
                self.generate_script
            ).pack(fill=tk.BOTH, expand=True)
        elif step == 5:
            RunScriptFrame(
                self.content_frame, 
                self.ahk_manager,
                self.run_script
            ).pack(fill=tk.BOTH, expand=True)
    
    def go_next(self):
        """Move to the next step."""
        if self.current_step < self.total_steps:
            # Validate before proceeding
            if not self.validate_current_step():
                return
                
            self.current_step += 1
            self.load_frame(self.current_step)
    
    def go_previous(self):
        """Move to the previous step."""
        if self.current_step > 1:
            self.current_step -= 1
            self.load_frame(self.current_step)
    
    def validate_current_step(self):
        """Validate the current step before proceeding."""
        if self.current_step == 1:
            # Check if AutoHotkey is installed
            if not self.ahk_manager.is_autohotkey_installed():
                messagebox.showerror(
                    "Missing Dependencies", 
                    "AutoHotkey must be installed before proceeding."
                )
                return False
                
            # Check if WhatsApp Desktop is installed or at least informed
            if not self.whatsapp_helper.is_whatsapp_notified():
                result = messagebox.askyesno(
                    "WhatsApp Desktop Required", 
                    "WhatsApp Desktop is required for this application. Have you installed it?"
                )
                if not result:
                    return False
                self.whatsapp_helper.set_whatsapp_notified(True)
        
        elif self.current_step == 2:
            # Check if coordinates were captured
            settings = get_settings(self.db_path)
            if not settings or settings['coordinate_x'] == 0 and settings['coordinate_y'] == 0:
                messagebox.showerror(
                    "Coordinates Required", 
                    "Please capture the coordinates for the WhatsApp message field before proceeding."
                )
                return False
        
        elif self.current_step == 3:
            # Check if security number was provided
            security_number = self.get_security_number_input()
            if not security_number:
                messagebox.showerror(
                    "Security Number Required", 
                    "Please enter a security number before proceeding."
                )
                return False
                
            # Save security number to database
            save_security_number(self.db_path, security_number)
        
        elif self.current_step == 4:
            # Check if messages were provided and CSV was processed
            phone_numbers = get_all_phone_numbers(self.db_path)
            if not phone_numbers:
                messagebox.showerror(
                    "Phone Numbers Required", 
                    "Please upload a CSV file with phone numbers before proceeding."
                )
                return False
                
            # Save message fields
            self.save_message_fields()
            
            # Generate script
            settings = get_settings(self.db_path)
            success, message = self.ahk_manager.generate_script(
                settings, 
                phone_numbers, 
                self.messages
            )
            
            if not success:
                messagebox.showerror("Script Generation Error", message)
                return False
                
            # Store script path for the next step
            self.script_path = message
        
        return True
    
    def update_status(self, message):
        """Update status message in the current frame."""
        # This would be implemented by each frame as needed
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'update_status'):
                widget.update_status(message)
    
    def capture_coordinates(self, x, y):
        """Save captured coordinates to the database."""
        save_coordinates(self.db_path, x, y)
        messagebox.showinfo(
            "Coordinates Captured", 
            f"Coordinates captured successfully: X={x}, Y={y}"
        )
    
    def get_security_number_input(self):
        """Get security number from the input field."""
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'get_security_number'):
                return widget.get_security_number()
        return ""
    
    def save_message_fields(self):
        """Save message fields to the messages dictionary."""
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'get_messages'):
                self.messages = widget.get_messages()
    
    def process_csv(self, file_path):
        """Process the CSV file and update the database."""
        success, message = process_csv_file(self.db_path, file_path)
        if success:
            messagebox.showinfo("CSV Processing", message)
            return True
        else:
            messagebox.showerror("CSV Processing Error", message)
            return False
    
    def generate_script(self):
        """Generate the AutoHotkey script based on user inputs."""
        settings = get_settings(self.db_path)
        phone_numbers = get_all_phone_numbers(self.db_path)
        
        # Save message fields first
        self.save_message_fields()
        
        success, message = self.ahk_manager.generate_script(
            settings, 
            phone_numbers, 
            self.messages
        )
        
        if success:
            messagebox.showinfo(
                "Script Generated", 
                "AutoHotkey script generated successfully."
            )
            return True
        else:
            messagebox.showerror("Script Generation Error", message)
            return False
    
    def run_script(self):
        """Run the generated AutoHotkey script."""
        if hasattr(self, 'script_path') and os.path.exists(self.script_path):
            success, message = self.ahk_manager.run_script(
                self.script_path, 
                self.update_status
            )
            
            if success:
                self.update_status("Script is running. Please do not interfere with the automation.")
                return True
            else:
                messagebox.showerror("Script Execution Error", message)
                return False
        else:
            messagebox.showerror(
                "Script Not Found", 
                "Please generate the script first in Step 4."
            )
            return False
