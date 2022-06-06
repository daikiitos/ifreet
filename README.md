# ifreet
iFreet is a web application for Twitter which allows you to make a tweet to be deleted at a specified time.

## Features
- Delete tweet at a specified time
- Cancel a delete reservation

## Requirements
- Twitter API v2
- Heroku
- Heroku Postgres (PostgreSQL)
- Python 3.10.3
- Flask 2.0.3
- Flask-SQLAlchemy 2.5.1
- gunicorn 20.1.0
- tweepy 4.7.0
- psycopg2 2.9.3
- APScheduler 3.9.1

## Usage
1. In Twitter Developer Potal, turn OAuth 1.0a on.
2. Set App permissons to Read and write and Callback URI / RedirectURL to https://***your_heroku_app_name***.herokuapp.com/callback.
> If you run the app in local, set a Callback URI to 127.0.0.1:5000.
3. Set WebsiteURL to the top page of your app, but another URL is acceptable.
4. Regenerate API Keys.
5. Install Heroku Postgres add-on.
6. Set Config Vars in Heroku settings. DATABASE_URL is automatically set, but it is obsolete, so set it or another variable to a URL starting with *postgresql://*.
- ACCESS_TOKEN: API Key
- ACCESS_TOKEN_SECRET: API Key Secret
- CALLBACK_URL: the URL you decided
- DB_URL or DATABASE_URL: Heroku Postgres URL
- CLOCK_INTERVAL: You should set this unless you run a delete program continuously.
- SECRET_KEY: Flask session secret key
7. Push your code into Heroku
8. Create table:
```
heroku run python
>>>from model import db
>>>db.create_all()
>>>quit()
```
9. Run app and clock
```
heroku ps:scale web=1 clock=1
```
