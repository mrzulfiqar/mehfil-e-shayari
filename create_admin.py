import sqlite3
import os
from werkzeug.security import generate_password_hash
from config import Config
import sys

def init_db():
    """Initializes the database if it doesn't exist."""
    print("--- Initializing Database ---")
    if not os.path.exists(os.path.dirname(Config.DATABASE)):
        os.makedirs(os.path.dirname(Config.DATABASE))
        
    try:
        conn = sqlite3.connect(Config.DATABASE)
        with open('database/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def create_admin():
    print("--- Create Admin User ---")
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty")
        return

    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty")
        return
        
    password_hash = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect(Config.DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        
        print(f"Success! Admin '{username}' created.")
        
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init_db() # Ensure DB is ready
    create_admin()
