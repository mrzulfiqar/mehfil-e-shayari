import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config
import sys

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
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        
        print(f"Success! Admin '{username}' created.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_admin()
