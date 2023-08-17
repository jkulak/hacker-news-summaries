from datetime import datetime
import os
import re
import sqlite3

from dotenv import load_dotenv
import requests

load_dotenv(override=True)

REQUEST_TIMEOUT = 10
HN_JSON_FEED_URL = os.getenv('HN_JSON_FEED_URL')


# Create or connect to hn.sqlite database
conn = sqlite3.connect("db/hn.sqlite3")
cursor = conn.cursor()


def create_table():
    """Create the table if it does not exist"""
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS hacker_news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hn_id INTEGER UNIQUE,
        title TEXT,
        content_html TEXT,
        url TEXT,
        external_url TEXT,
        date_published DATETIME,
        author_name TEXT,
        author_url TEXT,
        scraping_date DATETIME,
        comments_url TEXT,
        num_comments INTEGER,
        points INTEGER,
        comments_json TEXT,
        article_content_raw TEXT,
        article_content_extracted TEXT
    )
    """
    )


def extract_from_content_html(content_html):
    # Extracting comments URL and number of comments using regex
    comments_url = (
        re.search(r'Comments URL: <a href="(.*?)">', content_html).group(1)
        if re.search(r'Comments URL: <a href="(.*?)">', content_html)
        else None
    )
    num_comments = (
        int(re.search(r"# Comments: (\d+)", content_html).group(1))
        if re.search(r"# Comments: (\d+)", content_html)
        else None
    )

    points = (
        int(re.search(r"Points: (\d+)", content_html).group(1))
        if re.search(r"Points: (\d+)", content_html)
        else None
    )

    return comments_url, num_comments, points


def fetch_comments(url):
    response = requests.get(url)
    # Assuming the comments are returned in JSON format, although this might not be the case for Hacker News
    return response.text


def get_id_from_url(url):
    match = re.search(r"id=(\d+)$", url)
    return int(match.group(1)) if match else None


def main():
    create_table()
    response = requests.get(HN_JSON_FEED_URL, timeout=REQUEST_TIMEOUT)
    data = response.json()
    scraping_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in data["items"]:
        comments_url, num_comments, points = extract_from_content_html(
            item["content_html"]
        )
        # comments_data = fetch_comments(comments_url) if comments_url else None
        # we do not have a method for getting comments currently
        comments_data = ""
        article_content_raw = ""
        article_content_extracted = ""

        date_published = item.get("date_published")
        if date_published:
            date_published = datetime.fromisoformat(
                date_published.replace("Z", "")
            ).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT OR IGNORE INTO hacker_news (
            hn_id, title, content_html, url, external_url, date_published,
            author_name, author_url, scraping_date, comments_url, num_comments, comments_json,
            article_content_raw, article_content_extracted, points
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                get_id_from_url(item.get("id")),
                item.get("title"),
                item.get("content_html"),
                item.get("url"),
                item.get("external_url"),
                date_published,
                item.get("author", {}).get("name"),
                item.get("author", {}).get("url"),
                scraping_date,
                comments_url,
                num_comments,
                comments_data,
                article_content_raw,
                article_content_extracted,
                points,
            ),
        )

    # Commit the changes
    conn.commit()


if __name__ == "__main__":
    main()
    conn.close()
