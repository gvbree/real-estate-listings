from supabase import create_client
import config

def create_supabase_driver():
    url = config.SUPABASE_URL 
    key = config.SUPABASE_KEY
    supabase = create_client(url, key)
    print("Supabase driver created successfully.")

    return supabase