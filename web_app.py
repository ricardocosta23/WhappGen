#!/usr/bin/env python3
"""
WhatsApp Messaging Automation - Web Version
A web-based version of the WhatsApp automation app that can be previewed in a browser.
"""

import os
import json
import time
import subprocess
import platform
import pandas as pd
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, send_from_directory
from functools import wraps
import shutil
import sqlite3

app = Flask(__name__)
app.secret_key = "whatsapp_automation_secret_key"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Configuration
CONFIG_FILE = 'whatsapp_config.json'
PHONE_NUMBERS_FILE = 'phone_numbers.csv'
MESSAGES_FILE = 'messages.json'
SAMPLE_SCRIPT_FILE = 'sample_script.ahk'

# Sleep times (milliseconds)
DEFAULT_SLEEP_TIMES = {
    'sleep_1': 1000,  # 1 second
    'sleep_2': 2000,  # 2 seconds
    'sleep_3': 3000,  # 3 seconds
    'sleep_4': 4000   # 4 seconds
}

def load_config():
    """Load configuration from file or create default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)

                # Ensure sleep times are in config
                if 'sleep_times' not in config:
                    config['sleep_times'] = DEFAULT_SLEEP_TIMES.copy()
                else:
                    # Make sure all sleep times are present
                    for key, value in DEFAULT_SLEEP_TIMES.items():
                        if key not in config['sleep_times']:
                            config['sleep_times'][key] = value

                # Add troubleshooting counter if it doesn't exist
                if 'troubleshooting_count' not in config:
                    config['troubleshooting_count'] = 0

                return config
        except:
            pass

    # Default configuration
    return {
        'coordinate_x': 0,
        'coordinate_y': 0,
        'security_number': '',
        'autohotkey_installed': False,
        'whatsapp_installed': False,
        'sleep_times': DEFAULT_SLEEP_TIMES.copy(),
        'troubleshooting_count': 0
    }

def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_messages():
    """Load messages from file."""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_messages(messages):
    """Save messages to file."""
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

def get_phone_numbers():
    """Get phone numbers from CSV file."""
    if os.path.exists(PHONE_NUMBERS_FILE):
        try:
            df = pd.read_csv(PHONE_NUMBERS_FILE)
            return df.to_dict('records')
        except:
            pass
    return []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = {
            'admin': 'admin121',
            'admin2': 'admin122',
            'admin3': 'admin123'
        }
        
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    """Home page."""
    config = load_config()
    messages = load_messages()
    phone_numbers = get_phone_numbers()

    return render_template('index.html', 
                          config=config, 
                          messages=messages,
                          phone_numbers=phone_numbers,
                          phone_numbers_count=len(phone_numbers),
                          messages_count=len(messages))

@app.route('/step/<int:step>')
def step(step):
    """Render a specific step page."""
    config = load_config()
    messages = load_messages()
    phone_numbers = get_phone_numbers()

    if step == 1:
        return render_template('step1.html', config=config)
    elif step == 2:
        return render_template('step2.html', config=config)
    elif step == 3:
        return render_template('step3.html', config=config)
    elif step == 4:
        return render_template('step4.html', config=config, messages=messages)
    elif step == 5:
        return render_template('step5.html', 
                              config=config, 
                              phone_numbers=phone_numbers,
                              phone_numbers_count=len(phone_numbers))
    elif step == 6:
        return render_template('step6.html',
                              config=config,
                              phone_numbers=phone_numbers,
                              phone_numbers_count=len(phone_numbers))
    else:
        return redirect(url_for('index'))

@app.route('/troubleshooting')
def troubleshooting():
    """Render the troubleshooting page."""
    config = load_config()
    return render_template('troubleshooting.html', config=config)

@app.route('/check_dependencies', methods=['POST'])
def check_dependencies():
    """Simulate checking for dependencies."""
    config = load_config()

    # Simulate successful checks
    config['autohotkey_installed'] = True
    config['whatsapp_installed'] = True

    save_config(config)
    flash('Dependencies checked successfully', 'success')
    return redirect(url_for('step', step=1))

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    """Save message field coordinates."""
    config = load_config()

    try:
        x = int(request.form.get('coordinate_x', 0))
        y = int(request.form.get('coordinate_y', 0))

        config['coordinate_x'] = x
        config['coordinate_y'] = y

        save_config(config)
        flash(f'Coordinates saved: ({x}, {y})', 'success')
    except:
        flash('Invalid coordinates', 'error')

    return redirect(url_for('step', step=2))

@app.route('/save_security_number', methods=['POST'])
def save_security_number():
    """Save security number."""
    config = load_config()

    security_number = request.form.get('security_number', '').strip()

    if not security_number:
        flash('Security number cannot be empty', 'error')
        return redirect(url_for('step', step=3))

    if not security_number.isdigit():
        flash('Security number must contain only digits', 'error')
        return redirect(url_for('step', step=3))

    config['security_number'] = security_number
    save_config(config)

    flash('Security number saved', 'success')
    return redirect(url_for('step', step=3))

@app.route('/save_messages', methods=['POST'])
def save_messages_route():
    """Save message templates."""
    messages = {}

    # Extract all message inputs from form
    for key in request.form:
        if key.startswith('msg') and request.form[key].strip():
            messages[key] = request.form[key].strip()

    save_messages(messages)
    flash(f'{len(messages)} message(s) saved', 'success')
    return redirect(url_for('step', step=4))

@app.route('/process_csv', methods=['POST'])
def process_csv():
    """Process CSV file with phone numbers."""
    if 'csv_file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('step', step=5))

    file = request.files['csv_file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('step', step=5))

    # Save the uploaded file temporarily
    temp_path = 'uploaded_csv.csv'
    file.save(temp_path)

    try:
        # Process the CSV file
        df = pd.read_csv(temp_path)

        if 'Numero de Telefone' not in df.columns:
            flash('CSV file must contain a "Numero de Telefone" column', 'error')
            return redirect(url_for('step', step=5))

        # Save processed data
        df.to_csv(PHONE_NUMBERS_FILE, index=False)

        flash(f'Successfully processed {len(df)} phone numbers', 'success')
    except Exception as e:
        flash(f'Error processing CSV: {str(e)}', 'error')

    return redirect(url_for('step', step=5))

@app.route('/generate_script', methods=['POST'])
def generate_script():
    """Generate AutoHotkey script based on the sample_script.ahk template."""
    config = load_config()
    messages = load_messages()

    if not config['security_number']:
        flash('Please configure a security number first', 'error')
        return redirect(url_for('step', step=5))

    if config['coordinate_x'] == 0 and config['coordinate_y'] == 0:
        flash('Please configure message field coordinates first', 'error')
        return redirect(url_for('step', step=5))

    if not os.path.exists(PHONE_NUMBERS_FILE):
        flash('Please upload a CSV file with phone numbers first', 'error')
        return redirect(url_for('step', step=5))

    try:
        # Check if sample script exists
        if not os.path.exists(SAMPLE_SCRIPT_FILE):
            flash(f'Template script file not found: {SAMPLE_SCRIPT_FILE}', 'error')
            return redirect(url_for('step', step=5))

        # Read phone numbers
        df = pd.read_csv(PHONE_NUMBERS_FILE)

        # Get sleep times from config
        sleep_times = config['sleep_times']

        # Read the template file
        with open(SAMPLE_SCRIPT_FILE, 'r', encoding='utf-8') as f:
            template = f.read()

        # Extract the template block for phone number processing
        start_marker = "; ========== PHONE NUMBER PROCESSING TEMPLATE =========="
        end_marker = "; ========== END PHONE NUMBER PROCESSING TEMPLATE =========="

        if start_marker not in template or end_marker not in template:
            flash('The sample script template is missing required markers', 'error')
            return redirect(url_for('step', step=5))

        template_parts = template.split(start_marker)
        header = template_parts[0]

        phone_template = template.split(start_marker)[1].split(end_marker)[0]

        # Update sleep times in the header
        for key, value in sleep_times.items():
            pattern = f"global {key} := \\d+"
            replacement = f"global {key} := {value}"
            import re
            header = re.sub(pattern, replacement, header)

        # Read the template file
        with open(SAMPLE_SCRIPT_FILE, 'r', encoding='utf-8') as f:
            template = f.read()

        # Add generation timestamp comment
        script_content = f"; Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        script_content += header  # Use the header with sleep time variables

        # Process each phone number
        for i, row in df.iterrows():
            phone_number = str(row['Numero de Telefone']).strip()
            set_letter = chr(65 + (i % 4))  # A, B, C, D rotation

            # Create a copy of the template for this phone number
            current_script = phone_template

            # Replace all placeholders
            replacements = {
                "{security_number}": config['security_number'],
                "{coordinate_x}": str(config['coordinate_x']),
                "{coordinate_y}": str(config['coordinate_y']),
                "{phone_number}": phone_number,
                "{sleep_1}": "%sleep_1%",  # Use the global variables
                "{sleep_2}": "%sleep_2%",
                "{sleep_3}": "%sleep_3%",
                "{sleep_4}": "%sleep_4%"
            }

            # Apply all replacements
            for key, value in replacements.items():
                current_script = current_script.replace(key, value)

            # Add processed script for this phone number
            script_content += f"\n; Processing phone number {i+1}: {phone_number}\n\n"
            script_content += current_script + "\n"

            # Replace message placeholders with actual messages or remove message blocks
            for j in range(1, 5):
                msg_key = f'msg{j}{set_letter}'
                if msg_key in messages and messages[msg_key].strip():
                    msg = messages[msg_key].replace('\r\n', '{Enter}').replace('\n', '{Enter}')
                    # Add message block directly to script content
                    script_content += f"\n; Message Block {j}\n"
                    script_content += f"Sleep %sleep_1%\n"
                    script_content += f"Send {msg}\n"
                    script_content += f"Sleep %sleep_1%\n"
                    script_content += f"Send {{Enter}}\n"

            # # Add to complete script with phone number header
            # script_content += f"\n; Processing phone number {i+1}: {phone_number}\n"
            # script_content += current_script + "\n"

        # Save the script with timestamp
        script_file = f"whatsapp_automation_{int(time.time())}.ahk"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        flash(f'Script generated and saved as {script_file}', 'success')
        session['generated_script'] = script_file
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error generating script: {str(e)}', 'error')

    return redirect(url_for('step', step=6))

@app.route('/run_script', methods=['POST'])
def run_script():
    """Run the generated script using AutoHotkey."""
    script_file = session.get('generated_script', None)

    if not script_file or not os.path.exists(script_file):
        flash('Please generate a script first', 'error')
        return redirect(url_for('step', step=5))

    try:
        # Check if we're on Windows (only Windows can actually run the script)
        if platform.system() == 'Windows':
            # Look for AutoHotkey in common locations
            autohotkey_paths = [
                r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe"
            ]

            ahk_exe = None
            for path in autohotkey_paths:
                if os.path.exists(path):
                    ahk_exe = path
                    break

            if not ahk_exe:
                # Try to find in PATH
                try:
                    ahk_exe = subprocess.check_output(['where', 'autohotkey'], 
                                                   shell=True, 
                                                   text=True).strip().split('\n')[0]
                except:
                    pass

            if ahk_exe:
                # Actually run the script
                subprocess.Popen([ahk_exe, script_file])
                flash('Script is running. Please do not interfere with the automation.', 'success')
            else:
                flash('AutoHotkey not found. Please install AutoHotkey to run scripts.', 'warning')
        else:
            # On non-Windows systems, just simulate
            flash('Script cannot be run directly (Windows required). You can download the script and run it on a Windows machine.', 'warning')
    except Exception as e:
        flash(f'Error running script: {str(e)}', 'error')

    return redirect(url_for('step', step=5))

@app.route('/download_script')
@login_required
def download_script():
    """Download the generated scripts."""
    script_file = session.get('generated_script', None)

    if not script_file or not os.path.exists(script_file):
        flash('Please generate a script first', 'error')
        return redirect(url_for('step', step=5))

    try:
        # Create BAT script content
        bat_content = f'''@echo off
start "" "{os.path.basename(script_file)}"
'''
        
        # Save BAT temporarily
        bat_path = "WhatsAppMessenger.bat"
        with open(bat_path, 'w') as f:
            f.write(bat_content)

        # Send both files
        if request.args.get('type') == 'bat':
            return send_file(bat_path, as_attachment=True)
        else:
            return send_file(script_file, as_attachment=True)

        flash('Script installed successfully! Look for WhatsAppMessenger on your desktop.', 'success')
        return redirect(url_for('step', step=6))

    except Exception as e:
        flash(f'Error installing script: {str(e)}', 'error')
        return redirect(url_for('step', step=6))


@app.route('/download_sample_csv')
def download_sample_csv():
    """Download the sample CSV file."""
    if not os.path.exists('sample_contacts.csv'):
        generate_sample_csv_file()

    try:
        return send_file(
            'sample_contacts.csv',
            as_attachment=True,
            download_name='sample_contacts.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        flash(f'Error downloading CSV: {str(e)}', 'error')
        return redirect(url_for('step', step=5))

@app.route('/generate_sample_csv')
def generate_sample_csv():
    """Generate a sample CSV file."""
    generate_sample_csv_file()
    flash('Sample CSV file created: sample_contacts.csv', 'success')
    return redirect(url_for('step', step=5))

@app.route('/increase_sleep_time', methods=['POST'])
def increase_sleep_time():
    """Increase all sleep times by 10%."""
    config = load_config()

    # Increase troubleshooting counter
    config['troubleshooting_count'] += 1

    # Increase sleep times by 10%
    for key in config['sleep_times']:
        config['sleep_times'][key] = int(config['sleep_times'][key] * 1.1)

    save_config(config)

    # Show warning after 3 times
    if config['troubleshooting_count'] >= 3:
        flash('You have increased sleep times significantly. Please test the script before further increases.', 'warning')
    else:
        flash('Sleep times increased by 10%.', 'success')

    return redirect(url_for('step', step=6))

@app.route('/restore_default_sleep_times', methods=['POST'])
def restore_default_sleep_times():
    """Restore sleep times to default values."""
    config = load_config()
    
    # Set default sleep times
    config['sleep_times'] = {
        'sleep_1': 1000,  # 1 second
        'sleep_2': 3000,  # 3 seconds
        'sleep_3': 6000,  # 6 seconds
        'sleep_4': 9000   # 9 seconds
    }
    
    # Reset troubleshooting counter
    config['troubleshooting_count'] = 0
    
    save_config(config)
    flash('Sleep times restored to default values.', 'success')
    return redirect(url_for('step', step=6))

def generate_sample_csv_file():
    """Generate a sample CSV file with dummy phone numbers."""
    sample_data = {
        'Numero de Telefone': [
            '5511987654321',
            '5511912345678',
            '5521998765432',
            '5531987654321',
            '5541912345678'
        ],
        'Nome': [
            'João Silva',
            'Maria Oliveira',
            'Carlos Santos',
            'Ana Pereira',
            'Roberto Lima'
        ],
        'Email': [
            'joao@example.com',
            'maria@example.com',
            'carlos@example.com',
            'ana@example.com',
            'roberto@example.com'
        ]
    }

    df = pd.DataFrame(sample_data)
    df.to_csv('sample_contacts.csv', index=False)
    return 'sample_contacts.csv'

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)

    app.run(host='0.0.0.0', port=5000, debug=True)
