import requests
from bs4 import BeautifulSoup

def scrape_google_careers_jobs(url: str) -> list[dict]:
    """Google Careersの求人情報を取得する"""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    a_tags = soup.find_all("a", href=True)
    for a in a_tags:
        href = a["href"]
        aria_label = a.get("aria-label", "")
        if aria_label:
            if href.startswith("/"):
                href = "https://careers.google.com" + href
            jobs.append({
                "title": aria_label,
                "url": href
            })
    return jobs
