# WhatsApp Messaging Automation Tool

A Windows desktop application for automating WhatsApp message sending.

## Overview

This application allows you to automate sending WhatsApp messages to multiple contacts. It uses AutoHotkey to control your mouse and keyboard, making it possible to send messages through WhatsApp Desktop or WhatsApp Web.

![Application Screenshot](assets/screenshot.png)

## Features

- **Easy 5-Step Process**: Navigate through a simple, guided setup
- **CSV Import**: Send messages to multiple contacts from a CSV file
- **Message Templates**: Create and save message templates with variables
- **Automation**: Uses AutoHotkey to automate the message sending process
- **Coordinates Capture**: Visual tool to capture the exact position of the WhatsApp message input field

## System Requirements

- **Operating System**: Windows 10 or later
- **Python**: 3.6 or higher
- **Required Python Modules**:
  - pyautogui
  - pywin32
  - pandas
  - requests
  - tkinter (usually included with Python)
- **AutoHotkey**: Required for automation (installed automatically if missing)
- **WhatsApp Desktop or Web**: Must be installed and logged in

## Installation

### Easy Installation (Recommended)

1. Download the latest release from the [releases page](https://github.com/your-username/whatsapp-automation/releases)
2. Run the installer `WhatsAppAutomation-Setup.exe`
3. Follow the installation wizard

### Manual Installation

1. Clone the repository or download the source code
2. Ensure you have Python 3.6+ installed
3. Run the installer script:
   ```
   python install_windows.py
   ```
4. This will install all required dependencies

## Getting Started

1. Launch the application from the desktop shortcut or by running:
   ```
   python main.py
   ```
2. Follow the 5-step process:
   - **Step 1**: Setup - Check for required dependencies
   - **Step 2**: Coordinates - Capture the position of the WhatsApp message input field
   - **Step 3**: Security Number - Set a security number to prevent accidental message sending
   - **Step 4**: Messages - Configure your message templates
   - **Step 5**: Execute - Import contacts and run the script

## CSV Format

Your CSV file must contain a column named "Numero de Telefone" with phone numbers in international format (e.g., 551234567890). Additional columns can be used as variables in your message templates.

Example CSV format:
```csv
Numero de Telefone,Nome,Email
551234567890,John Doe,john@example.com
5512987654321,Jane Smith,jane@example.com
```

## How It Works

1. The application generates an AutoHotkey script based on your configuration
2. When executed, the script:
   - Opens WhatsApp Desktop/Web
   - Navigates to each contact
   - Types and sends your messages
   - Waits between messages to avoid being blocked

## Troubleshooting

### Screen Coordinates Not Working

If you're having issues with screen coordinates:

1. Ensure you have the latest version of PyAutoGUI and PyWin32
2. Run the installer script to check for missing dependencies:
   ```
   python install_windows.py
   ```
3. When capturing coordinates, make sure WhatsApp is fully visible on your screen
4. Try using an explicit coordinate value if the capture tool doesn't work

### AutoHotkey Not Working

1. Check if AutoHotkey is installed by running:
   ```
   autohotkey /?
   ```
2. If not installed, run the installer script or download AutoHotkey from [autohotkey.com](https://www.autohotkey.com/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and automation purposes only. Use responsibly and in accordance with WhatsApp's terms of service. Mass messaging may lead to your account being temporarily or permanently blocked.

## Support

If you encounter any issues, please open an issue on the GitHub repository with a detailed description of the problem.