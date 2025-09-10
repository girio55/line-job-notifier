from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_amazon_jobs(url: str) -> list[dict]:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # ページが完全に読み込まれるまで待機

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    jobs = []
    for tile in soup.select('div.job-tile'):
        link = tile.find("a", class_="job-link", href=True)
        if link:
            title = link.get_text(strip=True)
            href = link["href"]
            if not href.startswith("http"):
                href = "https://www.amazon.jobs" + href
            jobs.append({
                "title": title,
                "url": href
            })
    return jobs
