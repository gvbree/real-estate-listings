import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except (FileNotFoundError, KeyError, AttributeError):
        return os.getenv(key, default)

# Database Credentials
DB_USER = get_secret("DB_USER")
DB_PASSWORD = get_secret("DB_PASSWORD")
DB_HOST = get_secret("DB_HOST", "localhost")
DB_PORT = get_secret("DB_PORT", "5432")
DB_NAME = get_secret("DB_NAME")

# Supabase Credentials
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

# Other Configs
BASE_PATH = Path(__file__).resolve().parent
LISTINGS_PLATFORM_URL = get_secret("LISTINGS_PLATFORM_URL")
X_WH_CLIENT = get_secret("X_WH_CLIENT")
API_SEARCH_PATTERN = get_secret("API_SEARCH_PATTERN")