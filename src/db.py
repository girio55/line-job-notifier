import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URLまたはSUPABASE_KEYが設定されていません")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def is_job_in_db(job_url: str) -> bool:
    """求人URLがDBに存在するかチェック"""
    response = supabase.table("job_postings").select("id").eq("url", job_url).execute()
    return bool(response.data)

def save_job_to_db(job: dict, company: str):
    """新着求人をDBに保存"""
    data = {
        "company_name": company,
        "title": job["title"],
        "url": job["url"],
        "notified": False
    }
    supabase.table("job_postings").insert(data).execute()
