from app import Scraper

keyword = input("What do you want to search for? ")
keywords = keyword.split()

## create scraper object to scrape jobs in wanted website
scraper = Scraper(keywords)

for kw in scraper.keywords:
    db = scraper.scrape_jobs(kw)
    scraper.write_csv(kw, db)

