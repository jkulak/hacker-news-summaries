# Hacker News Summaries

This application shows summarized Hacker News articles with summarized comments.

## Requirements

* Python 3 or Docker
* ChatGPT API key

## Installation (how to install the application on a server)

1. Clone the respository on the server
1. Create `.env` from the template and fill in the environment variables
1. Install crontab from `deployment/crontab`

## Development (how to run the application locally)

It is suggested to use Docker to run the application locally. The following instructions assume that you have Docker installed.

You can also run the application using VS Code Dev Container. This will create a Docker container with all the dependencies installed and VS Code will connect to it. You can then run the application using the VS Code Run button.

```bash
# Create `.env` file and fill in the environment variables
cp .env.example .env

# Bulid the image
docker build -t hn src

# Create Docker network needed to communicate with Seleniarm chromium container
docker network create scraper-net

# Run the Seleniarm chromium container
docker run --rm -d --name chrome -p 4444:4444 -p 5900:5900 -p 7900:7900 --network scraper-net --shm-size 2g seleniarm/standalone-chromium:latest

# Run the articles grabber,
# this will create the database if it does not exist and grab articles
# from HN_JSON_FEED_URL and save it to SQlite database in DB_PATH
docker run --rm -v $(pwd):/app --env-file $(pwd)/.env --user $(id -u):$(id -g) hn python src/grab.py

# Run the article scraper,
# this will read 10 article URLs from the database with empty `article_content_raw` field
# and try to scrape the article content using Seleniarm chromium browser
docker run --rm -v $(pwd):/app --env-file $(pwd)/.env --user $(id -u):$(id -g) --network scraper-net hn python src/scrape.py

# Run the article content extractor,
# this will read 10 article URLs from the database with empty `article_content_extracted` field
# and try to extract the article content, by removing HTML, CSS, JS text
docker run --rm -v $(pwd):/app --env-file $(pwd)/.env --user $(id -u):$(id -g) hn python src/extract.py

# Run the article summarizer,
# this will read 10 article URLs from the database with empty `article_summary` field
# and try to summarize the article content using ChatGPT4
docker run --rm -v $(pwd):/app --env-file $(pwd)/.env --user $(id -u):$(id -g) hn python src/summarize.py

# TODO: Run the comments grabber,
# TODO: Run the comments summarizer,

# Run the www application,
# this will run the www application on http://localhost:8000
docker run --rm -v $(pwd):/app --env-file $(pwd)/.env --user $(id -u):$(id -g) -p 8000:8000 hn python src/www.py
```
