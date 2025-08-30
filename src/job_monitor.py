import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client
import json

# Supabaseクライアント作成（環境変数設定前提）
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_line_message(channel_access_token: str, to: str, message: str) -> bool:
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}"
    }
    payload = {
        "to": to,
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return True
    else:
        print(f"Failed to send LINE message: {response.status_code} {response.text}")
        return False

def scrape_google_careers_jobs(url: str) -> list[dict]:
    """Google Careersの求人一覧から求人名とURLを取得するサンプル"""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    # Google Careersの求人一覧のHTML構造に合わせて取得
    # 例として求人カードのaタグを探し、タイトルとリンクを取得
    for a in soup.select("a[jsname='job-card-link']"):  
        title = a.get_text(strip=True)
        job_url = "https://careers.google.com" + a.get("href")
        jobs.append({"title": title, "url": job_url})
    return jobs

def is_job_in_db(job_url: str) -> bool:
    """求人URLがすでにDBに存在するかチェック"""
    response = supabase.table("job_postings").select("id").eq("url", job_url).execute()
    return bool(response.data)

def save_job_to_db(job: dict):
    """新着求人をDBに保存"""
    data = {
        "title": job["title"],
        "url": job["url"],
        "notified": False  # 通知済みフラグ（必要に応じて）
    }
    supabase.table("job_postings").insert(data).execute()

def notify_new_job(job: dict):
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    if not channel_access_token or not user_id:
        raise RuntimeError("LINEの認証情報が設定されていません")

    message = f"新しい求人を発見しました！\n{job['title']}\n{job['url']}"
    if send_line_message(channel_access_token, user_id, message):
        print("LINEメッセージ送信成功")
    else:
        print("LINEメッセージ送信失敗")

def main():
    google_careers_url = "https://www.google.com/about/careers/applications/jobs/results/?hl=ja_jp&location=Tokyo%2C%20Japan"
    print("Google Careersの求人取得を開始します")

    jobs = scrape_google_careers_jobs(google_careers_url)
    print(f"取得した求人件数: {len(jobs)}")

    for job in jobs:
        if not is_job_in_db(job["url"]):
            print(f"新規求人を検知: {job['title']}")
            notify_new_job(job)
            save_job_to_db(job)
        else:
            print(f"既にDB登録済み: {job['title']}")

if __name__ == "__main__":
    main()
