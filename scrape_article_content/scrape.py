"""
Scrape article content from given url.
"""
import os
import sqlite3

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

load_dotenv(override=True)

REQUEST_TIMEOUT = 10
HN_JSON_FEED_URL = os.getenv("HN_JSON_FEED_URL")
DB_NAME = "hn.sqlite3"
CHROME_DRIVER_URL = "http://chrome:4444/wd/hub"

# Create or connect to hn.sqlite database
DB_PATH = os.getenv("DB_PATH")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create a Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
driver = webdriver.Remote(command_executor=CHROME_DRIVER_URL, options=options)


def get_content(url):
    """This code uses the Selenium Chrome driver to get the HTML content of the URL."""
    try:
        driver.get(url)
    except WebDriverException as exception:
        print(f"🥴 Error getting content for {url}: {exception}")
    html = driver.page_source
    return html


def update_content(hn_id, content):
    """This code updates the article_content_raw column for given article id."""
    cursor.execute(
        """
        UPDATE hacker_news
        SET article_content_raw = ?
        WHERE hn_id = ?
        """,
        (content, hn_id),
    )
    cursor.commit()


def main():
    """Select 10 rows where article_content_raw is NULL or empty"""
    cursor.execute(
        """
        SELECT hn_id, url
        FROM hacker_news
        WHERE COALESCE(article_content_raw, '') = ''
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    for row in rows:
        hn_id, url = row
        content = get_content(url)
        print(f"🔄 Updating content for {url}")
        update_content(hn_id, content)


if __name__ == "__main__":
    main()
    conn.close()
    driver.quit()
