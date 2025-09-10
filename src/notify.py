import os
import requests
import json

def send_line_message(channel_access_token: str, to: str, message: str) -> bool:
    """LINE Messaging APIでメッセージを送信する"""
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
        print("LINEメッセージ送信成功")
        return True
    else:
        print(f"LINEメッセージ送信失敗: {response.status_code} {response.text}")
        return False

def notify_new_job(job: dict, company: str):
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    if not channel_access_token or not user_id:
        raise RuntimeError("LINEの認証情報が設定されていません")
    message = (
        f"新しい求人を見つけたよ！\n"
        f"{company}\n"
        f"{job['title']}\n"
        f"\n"
        f"{job['url']}"
    )
    send_line_message(channel_access_token, user_id, message)
