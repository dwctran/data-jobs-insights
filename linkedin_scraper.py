import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters
import pandas as pd

# Change root logger level (default is WARN)
logging.basicConfig(level = logging.INFO)

jobs = []

def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.location, data.place, data.industries, data.date, data.link, data.insights, len(data.description_html))
    jobs.append({
        'title': data.title,
        'company': data.company,
        'place': data.place,
        'industries': data.industries,
        'job_function': data.job_function,
        'seniority_level': data.seniority_level,
        'description': [data.description.replace('\n', ' ')]
    })
    df = pd.DataFrame(jobs, index = None)
    df.to_csv('df_3.csv', encoding = 'UTF-8')

def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path="C:\\Users\\dinhd\\Downloads\\chromedriver_win32\\chromedriver.exe", # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query='data scientist',
        options=QueryOptions(
            locations=['Vietnam'],
            optimize=True,
            limit=300,
            filters=QueryFilters(
                relevance=RelevanceFilters.RELEVANT,
                time=TimeFilters.ANY,
                type=None,
                experience=None,
            )
        )
    ),
]

scraper.run(queries)
