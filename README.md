# PyBot
A simple Facebook Messenger Chatbot, powered by Flask.
## Video demo: [Here]()

## Table of content:

## Setup commands:
1. Install Pipenv:
> `pip install pipenv`

2. Install packages:
> `pipenv install`

3. (Optionally) Test the app:
> `pipenv run test`

4. Start the dev server:
> `pipenv run dev_server`

Deployment instructions coming soon.
## Project structure
- [`scripts`](./scripts/): These are the modules that powered the commands. Each modules corresponds to a command, as defined in [`utils.py`](./utils.py). 
- [`tests`](./tests/): Unit test files. In addition to testing all the commands in `scripts`, it also tests for the endpoints (defined in [`app.py`](app.py)) and the utility functions (defined in [`utils.py`](utils.py)).
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
