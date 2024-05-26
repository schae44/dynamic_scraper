from flask import Flask, render_template, request
from extractors.wanted import WantedScraper
from extractors.berlinstartupjobs import BerlinScraper
from extractors.wwr import WwrScraper
from extractors.web3 import Web3Scraper

app = Flask("Job Scraper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        # wanted_scraper = WantedScraper(keyword)
        # wanted = wanted_scraper.scrape_jobs(keyword)
        berlin_scraper = BerlinScraper(keyword)
        berlin = berlin_scraper.scrape_jobs(keyword)
        wwr_scraper = WwrScraper(keyword)
        wwr = wwr_scraper.scrape_jobs(keyword)
        web3_scraper = Web3Scraper(keyword)
        web3 = web3_scraper.scrape_jobs(keyword)
        jobs = berlin + wwr + web3
        db[keyword] = jobs
    return render_template("search.html", keyword = keyword, jobs = jobs)
