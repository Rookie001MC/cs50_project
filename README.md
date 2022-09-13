# CS50 Python Project: Messenger Assisstant
A simple Facebook Messenger Chatbot, powered by Flask.
## Video demo: [Here]()

## Requirements: 
- Python 3.9+
## Table of content:
- [CS50 Python Project: Messenger Assisstant](#cs50-python-project-messenger-assisstant)
  - [Video demo: Here](#video-demo-here)
  - [Requirements:](#requirements)
  - [Table of content:](#table-of-content)
  - [Installation:](#installation)
  - [Project structure](#project-structure)
  - [`app.py` endpoints:](#apppy-endpoints)
  - [Things that I still don't feel right with the app](#things-that-i-still-dont-feel-right-with-the-app)
  - [What I learned from the project](#what-i-learned-from-the-project)

## Installation:
***Note: You must have a Facebook Developer account to use this app.***
- Clone this repository.
- Copy `.env.example` then rename to `.env`
- Add the required values into the `.env` file:
  - `ACCESS_TOKEN`: This is the token of your Facebook app in the Developer page.
  - `VERIFY_TOKEN`: This is the token to verify the connection to your Facebook app. Can be any token of your choice.
  - `WEATHER_API_KEY`: This is the token from [OpenWeatherMap's API](https://openweathermap.org/api). 
  - Instructions for finding these can be found online.
- Install the dependencies:
  - Using `pip`: `pip install -r requirements-dev.txt`
  - Using `pipenv`: `pipenv install` 
- (Optionally) Test the app: `python -m pytest -vvv .`
- Run the app: `python project.py`


## Project structure
- [`scripts`](./scripts/): These are the modules that powered the commands. Each modules corresponds to a command, as defined in [`utils.py`](./utils.py). 
- [`tests`](./tests/): Unit test files. In addition to testing all the commands in `scripts`, it also tests for the endpoints (defined in [`app.py`](app.py)) and the utility functions (defined in [`utils.py`](utils.py)).
  - **Note**: only the [`fuel_price script`](./scripts/fuel_price.py) does not have its test file. Apparently it is very hard to test web-scraping scripts, and even more so with sites with dynamic data.
- [`web`](./web/): Mostly HTML files to serve the root endpoint. 
- [`.env.example`](./.env.example): Example environment variable file, which is used to store secret API tokens.
- [`.gitignore`](./.gitignore): Files specified here will be ignored by Git.
- [`Pipfile`](./Pipfile) and [`Pipfile.lock`](./Pipfile.lock): Files managed by Pipenv, similar to `package.json` and `package-lock.json` file for Node.js.
- [`project.py`](./project.py): Entry point to the application.
- [`Readme.md`](./README.md): This file!
- [`utils.py`](./utils.py): Some utilities functions to handle messages and more.

It is clear that I made this very modular, and for good reasons. This allows me to maintain each scripts individually, and makes it easy to manually test each features later on.

***Like all good web apps should be.***

## `app.py` endpoints:
- `/`: The root page, which as of now just renders a `index.html` file (with extra cats 🐱).
- `/webhook`: The main webhook endpoint, with support for GET and POST method for FB to use.
  - The `GET` method handles webhook verification when it is set up in FB's App Dashboard.
  - The `POST` method handles messages and postback events.
- `/webhook_dev`: This endpoint is used for development and manually testing the app using HTTP client apps like HTTPie or Postman.
- `/profile`: Doesn't do anything all by itself, but when accessed, either by using a browser or any HTTP client apps, it will setup the Messenger bot profile, using the Profile API.
Currently it is set up with a Get Started button, a Greeting text, and a Persistent Menu that links to my social profile.

## Things that I still don't feel right with the app
Though I am still an amateur programmer, there were so many design choices that I feel like it's not right. 
Some of these include:

- Forcing users to type subcommands, instead of letting them type the command, then wait for additional input. This can be seen clearly in the [`weather`](./scripts/weather.py) script, where they have to type the entire long command by themselves.
- Not allowing for multiple calls to the Send API. 
  - The current implementation of the Get Started button payload is that it sends all messages in a `for` loop, then delays for 2 seconds, then responds with a `200` code. I thought it would have been fine.
  - However, the Send API expects the `200` to be sent in a 20-second window. This implementation actually took **~17 seconds** to send a `200`! 
  - Were I to, in the future, add more messages, or execute a request, which would exceed the 20 seconds limit, that would cause quite a problem.
- Writing very ugly code, in my opinion. 
  - Obviously I can't complain too much, I am still not very good at programming, but sometimes it's hard to follow.

## What I learned from the project
All of the not-great things aside, I learned a lot from developing the project, such as:
- How to organize the project, time management,...
- How to write better code and better tests
- How to improve my problem solving
- How to document my code more clearer
- ...
  
In addition, I also learned a lot more things about Python, like:
- How to setup and run a web application
- How to use an API and process data from it
- How to use BeautifulSoup4 to scrape the web when an API isn't available.
- ...

And so much more throughout the CS50 Python course. 

I hope that in the future, I will be able to utilize what I have aquired from the course so that I can progress further into the future, be it at university, or in a career.
