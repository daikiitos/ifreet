from datetime import datetime, timedelta, timezone
import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import tweepy
import tweeting
import database
from model import db

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']

# request_token_url = 'https://api.twitter.com/oauth/request_token'
# authenticate_url = 'https://api.twitter.com/oauth/authenticate'
access_token_url = 'https://api.twitter.com/oauth/access_token'


app = Flask(__name__)

# session settings
app.secret_key = os.environ['SECRET_KEY']
app.permanent_session_lifetime = timedelta(minutes=15)

db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


@app.route('/')
def index():
    try:
        if 'access_token' in session:
            access_token = session['access_token']

            # get registerd Tweets
            twts = database.get_tweets(access_token['user_id'])

            if len(twts) != 0:
                # store tweet_id and delete_time
                dels = {}
                for twt in twts:
                    dels[int(twt.id)] = twt.delete_time
                
                # to display time
                JST =timezone(timedelta(hours=+9))
                # get registered tweets
                response = tweeting.get_tweets(list(dels.keys()), access_token['oauth_token'], access_token['oauth_token_secret'])
                # the return value is None
                response.data.reverse()

                return render_template('index.html', tweets=response.data, dels=dels, JST=JST)
                
    except Exception as e:
        flash(str(e))
        print('index: '+str(e))

    return render_template('index.html')


# make a tweet and register it
@app.route('/tweet', methods=['POST'])
def tweet():
    try:
        if 'access_token' in session:
            access_token = session['access_token']
            id = tweeting.do_tweet(request.form['text'], access_token['oauth_token'], access_token['oauth_token_secret'])

            if id is not None:
                tm = int(request.form['time'])
                if tm > 1440:
                    tm = 1440

                dt = datetime.now()
                td = timedelta(minutes=tm)
                dt += td
                
                database.insert_tweet(id, access_token['user_id'], dt)

    except Exception as e:
        flash(str(e))
        print('tweet: '+str(e))

    return redirect(url_for('index'))


# cancel registration
@app.route('/delete', methods=['GET'])
def delete():
    try:
        if 'access_token' in session:
            id = request.args.get('id')
            database.delete_tweet(id)

    except Exception as e:
        flash(str(e))
        print('delete: '+str(e))

    return redirect(url_for('index'))


# jump to an authenticateion page
@app.route('/auth')
def auth():
    try:
        # auth = OAuth1Session(consumer_key, consumer_secret)
        # response = auth.fetch_request_token(request_token_url)
        # authenticate_endpoint = '%s?oauth_token=%s' % (authenticate_url, response['oauth_token'])
        
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        redirect_url = auth.get_authorization_url()

        return redirect(redirect_url)
    except Exception as e:
        flash(str(e))
        print('auth: '+str(e))
        return redirect(url_for('index'))


# get an access_token
@app.route('/callback')
def callback():
    try:
        oauth_verifier = request.args.get('oauth_verifier')
        oauth_token = request.args.get('oauth_token')

        if oauth_verifier != None and oauth_token != None:
            auth = OAuth1Session(consumer_key, consumer_secret, oauth_token, oauth_verifier)
            response = auth.post(access_token_url, params={'oauth_verifier': oauth_verifier})
            access_token = dict(parse_qsl(response.content.decode('utf-8')))
            
            session['access_token'] = access_token

    except Exception as e:
        flash(str(e))
        print('callback: '+str(e))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)