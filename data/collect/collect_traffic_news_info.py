"""
This script collects traffic news information from RTHK Radio's traffic news webpage.
It starts fetching data from January 1, 2023, and aggregates news details including
date, time, and detail into a CSV file located at 'datasets/raw/traffic_news_info.csv'.
"""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]


def collect() -> None:
    """
    Collect traffic news information from RTHK's traffic news website and save it to a CSV file.

    This function retrieves traffic news data starting from January 1, 2023.
    It constructs URLs based on the date, fetches the web pages, and parses the HTML content
    to extract news articles. The extracted information includes the date, time, and details
    of each news item. All unique news entries are compiled into a pandas DataFrame and
    exported to a CSV file located at the designated dataset path.

    Returns:
        None
    """
    url_template = (
        "https://programme.rthk.hk/channel/radio/trafficnews/index.php?d={date}"
    )
    start_date = datetime(
        year=2010,
        month=1,
        day=1,
    )
    news_info_set = set()
    session = requests.Session()
    for i in tqdm(iterable=range(0, 3690)):
        date = (start_date + timedelta(days=i)).strftime(format="%Y%m%d")
        response = session.get(url=url_template.format(date=date))
        html = BeautifulSoup(
            markup=response.content,
            features="html.parser",
        )
        articles = html.find(
            name="div",
            class_="articles",
        )
        inner = (
            articles.find_all(
                name="li",
                class_="inner",
            )
            if articles
            else []
        )
        for info in inner:
            data = info.get_text().split("\t")
            date_time = data[-1].strip().split(" HKT ")
            if len(date_time) == 2:
                date, time = date_time
                detail = data[0]
                news_info_set.add((date, time, detail))
    df = pd.DataFrame(
        data=list(news_info_set),
        columns=["date", "time", "detail"],
    )
    print(df)
    df.to_csv(
        path_or_buf=f"{ROOT_DIR}/datasets/raw/traffic_news_info.csv",
        index=False,
    )


if __name__ == "__main__":
    collect()
