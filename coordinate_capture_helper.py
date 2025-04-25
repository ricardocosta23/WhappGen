import tkinter as tk
import pyautogui
import time
import sys

class CoordinateCaptureOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Semitransparent
        self.root.attributes('-topmost', True)
        
        # Make the window click-through
        self.root.wm_attributes('-transparentcolor', 'white')
        
        # Fill with white background
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create crosshair that follows mouse
        self.crosshair_h = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        self.crosshair_v = self.canvas.create_line(0, 0, 0, 0, fill='red', width=2)
        
        # Add text to show coordinates
        self.coord_text = self.canvas.create_text(10, 10, text="", fill='red', anchor=tk.NW, font=('Arial', 16, 'bold'))
        
        # Bind mouse motion to update crosshair
        self.root.bind('<Motion>', self.update_crosshair)
        
        # Bind escape to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Bind mouse click to capture and exit
        self.root.bind('<Button-1>', self.capture_and_exit)
        
        self.captured_x = 0
        self.captured_y = 0
        
    def update_crosshair(self, event):
        """Update crosshair position to follow mouse."""
        x, y = event.x, event.y
        
        # Update crosshair
        self.canvas.coords(self.crosshair_h, 0, y, self.root.winfo_width(), y)
        self.canvas.coords(self.crosshair_v, x, 0, x, self.root.winfo_height())
        
        # Update text
        self.canvas.itemconfig(self.coord_text, text=f"X: {x}, Y: {y}")
        
    def capture_and_exit(self, event):
        """Capture the coordinates and exit."""
        self.captured_x = event.x
        self.captured_y = event.y
        self.root.destroy()
        
    def run(self):
        """Run the overlay."""
        self.root.mainloop()
        return self.captured_x, self.captured_y


def capture_coordinates():
    """Run the coordinate capture tool and return the captured coordinates."""
    # Wait a moment to give user time to prepare
    print("Preparing coordinate capture overlay...")
    time.sleep(1)
    
    overlay = CoordinateCaptureOverlay()
    x, y = overlay.run()
    
    return x, y


if __name__ == "__main__":
    # If run directly, print the captured coordinates
    x, y = capture_coordinates()
    print(f"Captured coordinates: X={x}, Y={y}")
    
    # If arguments passed, write to a file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as f:
            f.write(f"{x},{y}")