from scraping import scrape_google_careers_jobs, scrape_amazon_jobs

SITES = [
    {
        "name": "Google",
        "func": scrape_google_careers_jobs,
        "url": "https://www.google.com/about/careers/applications/jobs/results/?hl=ja_jp&location=Tokyo%2C%20Japan"
    },
    {
        "name": "Amazon",
        "func": scrape_amazon_jobs,
        "url": (
            "https://amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi"
            "&radius=24km&latitude=35.6895&longitude=139.69172&loc_group_id=&loc_query=japan"
            "&base_query=Software%20Development&city=&country=JPN&region=&county=&query_options=&"
        )
    },
]
