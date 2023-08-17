# Hacker News Scraper

This is a Python application that scrapes the Hacker News best list and saves the articles to a SQLite database. The application is contained in a Docker container, so it can be easily deployed to any environment that has Docker installed.

## How to run the application locally

1. Clone the repository
2. Install Docker
3. Run the following command:

* `docker build -t hn_scraper .`
* `docker run -it --rm -v $(pwd):/app hn_scraper`

### Scraper

* `docker network create scraper-net`
* `docker run -d --name chrome -p 4444:4444 --network scraper-net selenium/standalone-chrome`

This will start the Docker container and run the application. The application will scrape the Hacker News best list and save the articles to a SQLite database called `hn.db`.

## How to deploy the application to an empty VM

1. Create an empty VM and install Docker
2. Copy the `Dockerfile` and the `hn_scraper` directory to the VM
3. Run the following command to build the Docker image:

`
docker build -t hn_scraper .
`

4. Run the following command to deploy the application:

`
docker run -it --rm -p 8080:8080 hn_scraper
`

This will start the Docker container and expose the application on port 8080. You can then access the application in your browser by going to `http://localhost:8080`.

## Python code

The Python code for the application is located in the `main.py` file. This file imports the necessary libraries and defines the functions that are used to scrape the Hacker News best list and save the articles to a SQLite database.

The main function of the application is the `scrape_hn()` function. This function takes the URL of the Hacker News best list as input and returns a list of articles. Each article in the list is a dictionary that contains the following information:

* ID
* Title
* URL
* Points
* Number of comments
* Comments URL

The `scrape_hn()` function uses the `requests` library to make an HTTP request to the Hacker News best list URL. The response is then parsed using the `BeautifulSoup` library. The article information is extracted from the HTML using `BeautifulSoup`'s `find_all()` method.

The `save_articles()` function takes a list of articles as input and saves them to a SQLite database. The database is created if it does not exist. The articles are saved to a table called `articles`. The table has the following columns:

* id
* title
* url
* points
* number_of_comments
* comments_url

The `comments_url` column contains the URL of the comments for the article. The `save_articles()` function uses the `requests` library to make an HTTP request to the comments URL. The response is then parsed using the `BeautifulSoup` library. The comments are extracted from the HTML using `BeautifulSoup`'s `find_all()` method. The comments are then saved to the `comments_json` column in the database.

I hope this helps! Let me know if you have any other questions.
