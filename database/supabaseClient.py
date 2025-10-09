from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Get the Supabase URL and key from the environment variables   
url: str = os.environ.get("SUPABASE_URL")
# Use service role key for server-side operations (bypasses RLS)
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
# results=supabase.table("Todo").select("*").execute()
# print(results)








