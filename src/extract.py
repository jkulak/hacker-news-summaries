"""
Extract content part of the articles, scarping html, css, javascript.
"""
import os
import re
import sqlite3

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(override=True)

NUM_ROWS = 10
REQUEST_TIMEOUT = 10
DB_PATH = os.getenv("DB_PATH")

# Create or connect to hn.sqlite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def update_content(hn_id, content):
    """This code updates the article_content_raw column for given article id."""
    cursor.execute(
        """
        UPDATE hacker_news
        SET
            article_content_extracted = ?,
            article_content_extracted_size = ?
        WHERE hn_id = ?
        """,
        (content, len(content), hn_id),
    )
    conn.commit()


def extract_plain_text(website_source):
    """Extract plain text from website source."""
    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(website_source, "html.parser")

    text = soup.get_text()

    # Remove source code snippets
    text = re.sub(r"<code.*?</code>", "", text, flags=re.DOTALL)

    # Remove style blocks
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)

    # Remove script blocks
    text = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove whitespace
    text = re.sub("\s+", " ", text).strip()

    print(f"📝 Extracted text legth: {len(text)}")

    return text


def main():
    """Select 10 rows where article_content_raw is NULL or empty"""
    cursor.execute(
        """
        SELECT hn_id, article_content_raw
        FROM hacker_news
        WHERE COALESCE(article_content_extracted, '') = ''
        LIMIT ?
        """,
        (NUM_ROWS,),
    )
    rows = cursor.fetchall()

    for row in rows:
        hn_id, content_raw = row
        print(f"🔄 Extracting content for {hn_id}")
        extracted_content = extract_plain_text(content_raw)
        update_content(hn_id, extracted_content)


if __name__ == "__main__":
    main()
    conn.close()
