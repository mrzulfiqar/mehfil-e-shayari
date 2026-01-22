import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_default_value_changeme')
    
    # Database Configuration (PostgreSQL via Supabase)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Ensure all required config is available (optional strict check)
