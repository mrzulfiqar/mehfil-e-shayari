import os
import psycopg2
from werkzeug.security import generate_password_hash
from config import Config

def create_admin():
    """Create an admin user in PostgreSQL database."""
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
        # Connect to PostgreSQL using DATABASE_URL
        conn = psycopg2.connect(Config.DATABASE_URL)
        cursor = conn.cursor()
        
        # Insert admin user (PostgreSQL uses %s for placeholders)
        cursor.execute(
            "INSERT INTO admins (username, password_hash) VALUES (%s, %s)", 
            (username, password_hash)
        )
        conn.commit()
        
        print(f"Success! Admin '{username}' created.")
        
        cursor.close()
        conn.close()
    except psycopg2.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_admin()
