"""
WhatsApp Messaging Automation - Web Version (Vercel Deployment)
A web-based version of the WhatsApp automation app, optimized for Vercel.
"""

import os
import json
import time
import subprocess  # Not directly usable on Vercel
import platform    # Limited use on Vercel
import pandas as pd
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, send_from_directory
from functools import wraps
import shutil # Not directly usable on Vercel
import sqlite3 # Not directly usable on Vercel

app = Flask(__name__)
app.secret_key = "whatsapp_automation_secret_key"

# Vercel Deployment Notes:
# ----------------------
# 1.  File System: Vercel's file system is read-only, except for /tmp.
#     -   Configuration files (whatsapp_config.json, phone_numbers.csv, messages.json) should be handled differently (e.g., environment variables, a database, or cloud storage).
#     -   Generated scripts cannot be saved to the file system.  Provide them for download only.
#     -   The sample CSV should be included directly.
# 2.  Dependencies:  Vercel uses serverless functions.
#     -   AutoHotkey:  Cannot be used on Vercel (Windows-specific, requires a running process).  The script generation is fine for *download*, but *not* execution.
#     -   pandas:  OK to use on Vercel.
#     -   sqlite3: OK to use, but the database file must be in /tmp.
# 3.  subprocess:  Cannot be used on Vercel.
# 4.  platform: Limited use.
# 5.  Session: Vercel supports sessions, but you might need to configure a specific store (like Redis) for persistence across invocations.  The default session mechanism might work for simple cases but isn't ideal for production.
# 6.  Templates and Static Files:  Flask's usual mechanisms work.
# 7.  Environment Variables: Use Vercel's environment variables for sensitive configuration (security number, etc.).
# 8.  Database:  If you need persistent data storage (for phone numbers, messages, etc.), consider a cloud database (e.g., PostgreSQL, MySQL on a service like Vercel Postgres, or a NoSQL database like MongoDB).
# 9. Vercel KV: For simple data storage, consider using Vercel KV.

# ===============================
# Configuration (Vercel Adaptations)
# ===============================

# Use a dictionary for default sleep times
DEFAULT_SLEEP_TIMES = {
    'sleep_1': 1000,
    'sleep_2': 2000,
    'sleep_3': 3000,
    'sleep_4': 4000
}

def load_config():
    """
    Load configuration.  On Vercel, prefer environment variables.
    This version loads defaults and merges in environment variables.
    """
    config = {
        'coordinate_x': int(os.environ.get('COORDINATE_X', 0)),
        'coordinate_y': int(os.environ.get('COORDINATE_Y', 0)),
        'security_number': os.environ.get('SECURITY_NUMBER', ''),
        'autohotkey_installed': False,  # Always False on Vercel
        'whatsapp_installed': False,    # Always False on Vercel
        'sleep_times': DEFAULT_SLEEP_TIMES.copy(),
        'troubleshooting_count': 0
    }

    # Load sleep times from environment variables if available
    for key in DEFAULT_SLEEP_TIMES:
        env_value = os.environ.get(key.upper())  # e.g., SLEEP_1
        if env_value:
            try:
                config['sleep_times'][key] = int(env_value)
            except ValueError:
                print(f"Warning: Invalid value for {key} in environment: {env_value}")

    return config

def save_config(config):
    """
    Save configuration.  *NOT* directly to a file on Vercel.
    This function is adapted to do nothing, or, if you have a Vercel KV, you can save it there.
    """
    #  On Vercel, you would typically use a database or Vercel KV.
    #  For this example, we'll just print a warning.
    print("Warning: save_config is not saving to a file on Vercel.  Consider using Vercel KV or a database.")
    # Example of using Vercel KV (install @vercel/kv)
    # from vercel_kv import kv
    # await kv.set("my-config", config)

def load_messages():
    """
    Load messages.  From a file (if present), or ideally, a database or Vercel KV.
    """
    #  Vercel Example (Vercel KV)
    # from vercel_kv import kv
    # messages = await kv.get("messages")
    # if messages:
    #   return messages
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_messages(messages):
    """
    Save messages.  *NOT* to a file on Vercel.  Use a database or Vercel KV.
    """
    # Vercel KV Example
    # from vercel_kv import kv
    # await kv.set("messages", messages)
    print("Warning: save_messages is not saving to a file on Vercel.  Consider using Vercel KV or a database.")
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

def get_phone_numbers():
    """
    Get phone numbers.  From a CSV file (if present), or, ideally, a database.
    """
    # Vercel KV Example
    # from vercel_kv import kv
    # phone_numbers = await kv.get("phone_numbers")
    # if phone_numbers:
    #   return phone_numbers
    if os.path.exists(PHONE_NUMBERS_FILE):
        try:
            df = pd.read_csv(PHONE_NUMBERS_FILE)
            return df.to_dict('records')
        except:
            pass
    return []

# ===============================
# Flask Routes
# ===============================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

    # Simulate successful checks (Always True for this Vercel version)
    config['autohotkey_installed'] = False # Changed to False
    config['whatsapp_installed'] = False # Changed to False

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

    try:
        # Process the CSV file directly from memory
        df = pd.read_csv(file)

        if 'Numero de Telefone' not in df.columns:
            flash('CSV file must contain a "Numero de Telefone" column', 'error')
            return redirect(url_for('step', step=5))

        # Save processed data (ideally to a database or Vercel KV)
        # For this example, we'll keep it in a variable (it will be lost on serverless function restart)
        # df.to_csv(PHONE_NUMBERS_FILE, index=False) # Removed saving to file

        # Store in session (for demonstration, will be lost between invocations)
        session['phone_numbers_data'] = df.to_dict(orient='records')
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

    # if not os.path.exists(PHONE_NUMBERS_FILE): # Removed file check
    #     flash('Please upload a CSV file with phone numbers first', 'error')
    #     return redirect(url_for('step', step=5))
    if 'phone_numbers_data' not in session:
        flash('Please upload a CSV file with phone numbers first', 'error')
        return redirect(url_for('step', step=5))

    try:
        # Check if sample script exists
        if not os.path.exists(SAMPLE_SCRIPT_FILE):
            flash(f'Template script file not found: {SAMPLE_SCRIPT_FILE}', 'error')
            return redirect(url_for('step', step=5))

        # Read phone numbers from session
        # df = pd.read_csv(PHONE_NUMBERS_FILE) # Removed file reading
        df = pd.DataFrame(session['phone_numbers_data'])

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
            script_content += f"\n; Processing phone number {i + 1}: {phone_number}\n\n"
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

        # Save the script with timestamp (IN MEMORY for Vercel)
        script_file_name = f"whatsapp_automation_{int(time.time())}.ahk"
        # In a real Vercel app, you might store this in Vercel KV if needed.
        session['generated_script_content'] = script_content
        session['generated_script_name'] = script_file_name

        flash(f'Script generated.  Click "Download Script" to save it.', 'success')
        return redirect(url_for('step', step=6))

    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error generating script: {str(e)}', 'error')
        return redirect(url_for('step', step=5))

@app.route('/run_script', methods=['POST'])
def run_script():
    """
    Run the generated script using AutoHotkey.  *CANNOT WORK ON VERCEl*.
    This route is modified to provide a warning.
    """
    # script_file = session.get('generated_script', None) # Removed file
    #
    # if not script_file or not os.path.exists(script_file): #Removed file check
    #     flash('Please generate a script first', 'error')
    #     return redirect(url_for('step', step=5))

    flash('Running the script on Vercel is not supported.  Download the script and run it on a Windows machine with AutoHotkey installed.', 'warning')
    return redirect(url_for('step', step=5))

@app.route('/download_script')
@login_required
def download_script():
    """Download the generated script."""
    # script_file = session.get('generated_script', None) # Removed file
    #
    # if not script_file or not os.path.exists(script_file): # Removed file check
    #     flash('Please generate a script first', 'error')
    #     return redirect(url_for('step', step=5))
    script_content = session.get('generated_script_content')
    script_name = session.get('generated_script_name')

    if not script_content or not script_name:
        flash('Please generate a script first.', 'error')
        return redirect(url_for('step', step=6))

    try:
        #  Instead of saving to a file, we create a response directly.
        #  Vercel example
        response =  app.make_response(script_content)
        response.headers["Content-Disposition"] = f"attachment; filename={script_name}"
        response.headers["Content-type"] = "text/plain"
        return response

    except Exception as e:
        flash(f'Error downloading script: {str(e)}', 'error')
        return redirect(url_for('step', step=6))

@app.route('/download_sample_csv')
def download_sample_csv():
    """Download the sample CSV file."""
    # if not os.path.exists('sample_contacts.csv'): # Removed file check
    #     generate_sample_csv_file()
    #
    # try:
    #     return send_file(
    #         'sample_contacts.csv',
    #         as_attachment=True,
    #         download_name='sample_contacts.csv',
    #         mimetype='text/csv'
    #     )
    # except Exception as e:
    #     flash(f'Error downloading CSV: {str(e)}', 'error')
    #     return redirect(url_for('step', step=5))
    try:
        # Directly send the file.
        return send_file(
            'sample_contacts.csv',  # Ensure this file is in your project root or a 'static' folder.
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
        'sleep_4': 9000  # 9 seconds
    }

    # Reset troubleshooting counter
    config['troubleshooting_count'] = 0

    save_config(config)
    flash('Sleep times restored to default values.', 'success')
    return redirect(url_for('step', step=6))

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Create static directory if it doesn'texist
    os.makedirs('static', exist_ok=True)
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
