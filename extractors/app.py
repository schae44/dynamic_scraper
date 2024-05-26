from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class Scraper:
    def __init__(self, keywords):
        self.keywords = keywords
   
    def write_csv(self, keyword, jobs_db):
        file = open(f"{keyword}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Reward', 'Link'])

        for job in jobs_db:
            writer.writerow(job.values())
        file.close()


