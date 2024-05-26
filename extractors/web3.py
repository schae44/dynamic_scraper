from extractors.app import Scraper
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class Web3Scraper(Scraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def scrape_jobs(self, keyword):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = f"https://web3.career/{keyword}-jobs"
        page.goto(url)

        content = page.content()
        p.stop()
        soup = BeautifulSoup(content, "html.parser")
        jobs_db = []

        jobs = soup.find_all("tr", {"data-jobid" : True})
        for job in jobs:
            link = f"https://web3.career{job.find('a', href = True)['href']}"
            title = job.find('h2').text
            company = job.find('h3').text
            region = job.find_all('td', class_ = "job-location-mobile")[1].text

            job = {
                "title": title,
                "company": company,
                "region" : region,
                "link": link
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
    


temp = Web3Scraper(['python'])
t = temp.scrape_jobs("python")


