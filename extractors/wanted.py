from extractors.app import Scraper
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class WantedScraper(Scraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def scrape_jobs(self, keyword):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = f"https://www.wanted.co.kr/search?query={keyword}&tab=position"
        page.goto(url)

        # time.sleep(5)
        # page.click("button.Aside_searchButton__Xhqq3")
        # time.sleep(5)
        # page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
        # time.sleep(5)
        # page.keyboard.down("Enter")
        # time.sleep(5)
        # page.click("a#search_tab_position")
        # for i in range(5):
        #     time.sleep(5)
        #     page.keyboard.down("End")

        content = page.content()
        p.stop()
        soup = BeautifulSoup(content, "html.parser")
        jobs_db = []

        jobs = soup.find_all("div", class_ = "JobCard_container__FqChn")
        for job in jobs:
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            title = job.find("strong", class_ = "JobCard_title__ddkwM").text
            company = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
            reward = job.find("span", class_ = "JobCard_reward__sdyHn").text 

            job = {
                "title": title,
                "company_name": company,
                "reward": reward,
                "link": link
            }
            jobs_db.append(job)
        return jobs_db
    

