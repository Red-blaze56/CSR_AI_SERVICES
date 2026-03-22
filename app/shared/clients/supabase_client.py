from supabase import create_client, Client
from app.core.config import CONFIG

url: str = CONFIG.SUPABASE_URL
key: str = CONFIG.SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)