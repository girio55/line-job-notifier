import os
from sites import SITES
from notify import notify_new_job
from db import is_job_in_db, save_job_to_db

def main():
    for source in SITES:
        print(f"{source['name']}の求人を取得中...")
        try:
            jobs = source["func"](source["url"])
        except Exception as e:
            print(f"{source['name']}の求人取得でエラー: {e}")
            continue

        print(f"{source['name']}の求人件数: {len(jobs)}")
        for job in jobs:
            if not is_job_in_db(job["url"]):
                print(f"新着求人: {job['title']}")
                try:
                    notify_new_job(job, source["name"])
                except Exception as e:
                    print(f"LINE通知でエラー: {e}")
                try:
                    save_job_to_db(job, source["name"])
                except Exception as e:
                    print(f"DB保存でエラー: {e}")
            else:
                print(f"既存求人: {job['title']}")

if __name__ == "__main__":
    main()
