"""
This script collects road data from a specified URL and saves it to a CSV file.
It sends a GET request to the given URL, processes the JSON response to extract
road information, and stores the data in a CSV file within the raw datasets directory.
"""

from pathlib import Path

import pandas as pd
import requests

ROOT_DIR = Path(__file__).resolve().parents[2]


def collect() -> None:
    """
    Collects road data from the given URL and saves it to a CSV file.

    Sends a GET request to the URL, processes the JSON response to extract road data,
    and saves the data into a CSV file located in the raw datasets directory.

    Returns:
        None
    """
    url = "https://www.overview.hk/street/ssp.php"
    response = requests.get(url=url)
    data = response.json()["data"]
    df = pd.DataFrame(
        data=data,
        columns=[
            "Name (Chinese)",
            "Name (English)",
            "Location (Chinese)",
            "Location (English)",
            "Additional Info",
        ],
    )
    print(df)
    df.to_csv(
        path_or_buf=f"{ROOT_DIR}/datasets/raw/roads_info.csv",
        index=False,
    )


if __name__ == "__main__":
    collect()
