from extractors.app import Scraper
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class WwrScraper(Scraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def scrape_jobs(self, keyword):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
        page.goto(url)

        content = page.content()
        p.stop()
        soup = BeautifulSoup(content, "html.parser")
        jobs_db = []

        jobs = soup.find_all("section", class_="jobs")
        for job in jobs:
            title = job.find("span", class_="title").text
            company = job.find("span", class_="company").text
            region = job.find("span", class_="region company").text
            url = job.find_all("a")[3]["href"]
            job = {
                "title": title,
                "company": company,
                "region": region,
                "link": f"https://weworkremotely.com{url}"
            }
            jobs_db.append(job)
        return jobs_db
    
    def write_csv(self, keyword, jobs_db):
        file = open(f"{keyword}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Region', 'Link'])

        for job in jobs_db:
            writer.writerow(job.values())
        file.close()
    

