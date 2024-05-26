from extractors.app import Scraper
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class BerlinScraper(Scraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def scrape_jobs(self, keyword):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
        page.goto(url)

        content = page.content()
        p.stop()
        soup = BeautifulSoup(content, "html.parser")
        jobs_db = []

        jobs = soup.find_all("div", class_="bjs-jlid__wrapper")

        for job in jobs:
            title = job.find("h4", class_="bjs-jlid__h").get_text()
            company = job.find("a", class_="bjs-jlid__b").get_text()
            # description = job.find(
            #     "div", class_="bjs-jlid__description").get_text().strip()
            url = job.find("h4", class_="bjs-jlid__h").find("a")["href"]
        
            job = {
                    "title": title,
                    "company": company,
                    "region": "Berlin, Germany",
                    "link": url
                }

            jobs_db.append(job)
        return jobs_db
    
    def write_csv(self, keyword, jobs_db):
        file = open(f"{keyword}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Description', 'Link'])

        for job in jobs_db:
            writer.writerow(job.values())
        file.close()

