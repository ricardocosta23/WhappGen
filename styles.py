import tkinter as tk
from tkinter import ttk
import os

def apply_styles(root):
    """Apply styles to the application."""
    style = ttk.Style()
    
    # Configure the theme
    try:
        style.theme_use('vista')  # Use native Windows theme if available
    except:
        pass  # Fallback to default theme
    
    # Configure common styles
    style.configure('TLabel', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10))
    style.configure('TEntry', font=('Arial', 10))
    style.configure('TFrame', background='#f0f0f0')
    
    # Configure accent button style
    style.configure('Accent.TButton', 
                    font=('Arial', 10, 'bold'),
                    background='#007bff',
                    foreground='white')
    
    # Configure header style
    style.configure('Header.TLabel', 
                    font=('Arial', 12, 'bold'),
                    foreground='#007bff')
    
    # Configure the title style
    style.configure('Title.TLabel', 
                    font=('Arial', 16, 'bold'),
                    foreground='#007bff')
                    
    # Configure LabelFrame styles
    style.configure('TLabelframe', 
                    background='#f0f0f0')
    style.configure('TLabelframe.Label', 
                    font=('Arial', 10, 'bold'),
                    foreground='#505050')
    
    # Add some padding to widgets
    style.configure('TFrame', padding=5)
    style.configure('TLabelframe', padding=10)
    
    # Set window icon if available
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'assets', 'logo.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass  # Skip icon setting if not available
    
    return style
