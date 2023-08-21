"""
Extract content part of the articles, scarping html, css, javascript.
"""
import os
import sqlite3

from dotenv import load_dotenv
import openai

load_dotenv(override=True)

NUM_ROWS = 1
REQUEST_TIMEOUT = 10
DB_PATH = os.getenv("DB_PATH")
GPT_API_URL = "https://api.openai.com/v1/chat/completions"

# Create or connect to hn.sqlite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

openai.api_key = os.getenv("OPENAI_API_KEY")


def update_content(hn_id, content):
    """This code updates the article_content_raw column for given article id."""
    cursor.execute(
        """
        UPDATE hacker_news
        SET article_content_extracted = ?
        WHERE hn_id = ?
        """,
        (content, hn_id),
    )
    conn.commit()


def extract_with_gpt(api_input):
    """Get a response from ChatGPT API."""
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a system that removes all html tags, css and javascript from given content and returns only text content that can be later summarized.",
            },
            {
                "role": "user",
                "content": "Extract main content from the text, removing all html, css, javascript and everything else that is not main content, return plain text only from: \n\n"
                + api_input,
            },
        ],
    )

    return chat.choices[0].message.content


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
        extracted_content = extract_with_gpt(content_raw)
        update_content(hn_id, extracted_content)


if __name__ == "__main__":
    main()
    conn.close()
