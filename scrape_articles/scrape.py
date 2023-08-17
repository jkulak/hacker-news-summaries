import os
import sqlite3

from dotenv import load_dotenv
from selenium import webdriver

load_dotenv(override=True)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
REQUEST_TIMEOUT = 10
HN_JSON_FEED_URL = os.getenv("HN_JSON_FEED_URL")
DB_NAME = "hn.sqlite3"
CHROME_DRIVER_URL = "http://chrome:4444/wd/hub"


# Create or connect to hn.sqlite database
db_path = os.path.join(SCRIPT_PATH, "..", "db", DB_NAME)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Create a Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Remote(command_executor=CHROME_DRIVER_URL, options=options)


# Sample get_content function
def get_content(url):
    driver.get("https://example.com")
    html = driver.page_source
    # Your logic here to get content from the URL
    return "content from the URL"


def update_content(db_conn, hn_id, content):
    cursor = db_conn.cursor()
    cursor.execute(
        """
        UPDATE hacker_news
        SET article_content_raw = ?
        WHERE hn_id = ?
        """,
        (content, hn_id),
    )
    db_conn.commit()


def main():
    # Select 10 rows where article_content_raw is NULL or empty
    cursor.execute(
        """
        SELECT hn_id, external_url
        FROM hacker_news
        WHERE COALESCE(article_content_raw, '') = ''
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    for row in rows:
        hn_id, url = row
        content = get_content(url)
        print(f"Updating content for {url}...")
        update_content(conn, hn_id, content)


if __name__ == "__main__":
    main()
    conn.close()
