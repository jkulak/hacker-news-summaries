import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask
from flask import render_template_string

load_dotenv(override=True)

app = Flask(__name__)
DB_PATH = os.getenv("DB_PATH")


@app.route("/")
def list_articles():
    articles = fetch_articles()

    template = """
    <!doctype html>
    <html>
    <head>
        <title>Articles List</title>
    </head>
    <body>
        {% for article in articles %}
        <div style="border: 1px solid black; margin: 10px; padding: 10px;">
            <h2>{{ article.title }}</h2>
            <p>{{ article.content }}</p>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(template, articles=articles)


def fetch_articles():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, article_content_extracted as content FROM hacker_news"
        )
        articles = cursor.fetchall()
    return articles


if __name__ == "__main__":
    app.run(debug=True)
