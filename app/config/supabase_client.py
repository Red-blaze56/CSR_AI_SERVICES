from supabase import create_client, Client
from app.config.settings import CONFIG

supabase: Client = create_client(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_SERVICE_KEY)