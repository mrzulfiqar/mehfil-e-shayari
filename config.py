import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_default_value_changeme')
    
    # Database Configuration
    DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'mehfil.db')
    
    # Ensure all required config is available (optional strict check)
