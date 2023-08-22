#!/bin/bash

NOW=$(date '+%Y-%m-%d-%H:%M:%S')
echo $NOW "Running scraper script"

APP_DIR=$HOME/hacker-news-summaries
DB_FILE=$HOME/db/db.sqlite3

docker run --rm -v $APP_DIR:/app \
    --env-file $APP_DIR/.env \
    --network scraper-net \
    --user $(id -u):$(id -g) hn python ./scrape_article_content/scrape.py

# docker run --rm -v /home/hn/hacker-news-summaries:/app --env-file /home/hn/hacker-news-summaries/.env --user $(id -u):$(id -g) hn python ./scrape_article_content/scrape.py
