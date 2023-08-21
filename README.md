# Hacker News Scraper

This is a Python application that scrapes the Hacker News best list and saves the articles to a SQLite database. The application is contained in a Docker container, so it can be easily deployed to any environment that has Docker installed.

## About

This project is using https://github.com/seleniumhq-community/docker-seleniarm to render the website and grab its full content.

## How to run the application locally

1. Clone the repository
2. Install Docker
3. Run the following command:

* `docker build -t hn_scraper .`
* `docker run -it --rm -v $(pwd):/app hn_scraper`

### Scraper

* `docker network create scraper-net`
* `docker run --rm -it --name chrome -p 4444:4444 -p 5900:5900 -p 7900:7900 --network= scraper-net --shm-size 2g seleniarm/standalone-chromium:latest`

This will start the Docker container and run the application. The application will scrape the Hacker News best list and save the articles to a SQLite database called `hn.sqlite3`.
