import sqlite3
import pandas as pd
import time
from datetime import datetime

def setup_database(db_path):
    """Create the SQLite database and tables if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        coordinate_x INTEGER DEFAULT 0,
        coordinate_y INTEGER DEFAULT 0,
        security_number TEXT DEFAULT ''
    )''')

    # Add default users
    default_users = [
        ('admin', 'admin121'),
        ('admin2', 'admin122'),
        ('admin3', 'admin123')
    ]
    
    for username, password in default_users:
        cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
                      (username, password))
    
    # Create phone numbers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phone_numbers (
        numero_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_telefone TEXT UNIQUE,
        date_timestamp INTEGER,
        envios INTEGER DEFAULT 0
    )
    ''')
    
    # Create settings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        coordinate_x INTEGER,
        coordinate_y INTEGER,
        security_number TEXT,
        last_updated INTEGER
    )
    ''')
    
    # Insert default settings if not exists
    cursor.execute('''
    INSERT OR IGNORE INTO settings (id, coordinate_x, coordinate_y, security_number, last_updated)
    VALUES (1, 0, 0, '', ?)
    ''', (int(time.time()),))
    
    conn.commit()
    conn.close()

def save_coordinates(db_path, x, y):
    """Save the captured coordinates to the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE settings
    SET coordinate_x = ?, coordinate_y = ?, last_updated = ?
    WHERE id = 1
    ''', (x, y, int(time.time())))
    
    conn.commit()
    conn.close()

def save_security_number(db_path, security_number):
    """Save the security number to the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE settings
    SET security_number = ?, last_updated = ?
    WHERE id = 1
    ''', (security_number, int(time.time())))
    
    conn.commit()
    conn.close()

def get_settings(db_path):
    """Get all settings from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT coordinate_x, coordinate_y, security_number FROM settings WHERE id = 1')
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            'coordinate_x': result[0],
            'coordinate_y': result[1],
            'security_number': result[2]
        }
    return None

def process_csv_file(db_path, csv_file_path):
    """Process the CSV file and update the database."""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Check if the required column exists
        if 'Numero de Telefone' not in df.columns:
            return False, "CSV file must contain a 'Numero de Telefone' column."
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        current_time = int(time.time())
        
        # Process each phone number
        for _, row in df.iterrows():
            phone_number = str(row['Numero de Telefone']).strip()
            
            # Skip empty or invalid entries
            if not phone_number:
                continue
                
            # Check if the number exists
            cursor.execute(
                'SELECT numero_ID, envios FROM phone_numbers WHERE numero_telefone = ?', 
                (phone_number,)
            )
            result = cursor.fetchone()
            
            if result:
                # Update existing number
                cursor.execute(
                    'UPDATE phone_numbers SET date_timestamp = ?, envios = ? WHERE numero_ID = ?',
                    (current_time, result[1] + 1, result[0])
                )
            else:
                # Insert new number
                cursor.execute(
                    'INSERT INTO phone_numbers (numero_telefone, date_timestamp, envios) VALUES (?, ?, 0)',
                    (phone_number, current_time)
                )
        
        conn.commit()
        conn.close()
        return True, f"Successfully processed {len(df)} phone numbers."
    
    except Exception as e:
        return False, f"Error processing CSV file: {str(e)}"

def get_all_phone_numbers(db_path):
    """Get all phone numbers from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT numero_ID, numero_telefone, envios FROM phone_numbers ORDER BY numero_ID')
    results = cursor.fetchall()
    
    conn.close()
    
    return results
