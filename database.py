from datetime import datetime
from flask import flash, session
from model import Tweet, User
from model import db
# from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.dialects.postgresql import insert

# get up to 20 registerd Tweets 
def get_tweets(user_id):
    try:
        tweets = Tweet.query.filter_by(user_id=user_id).limit(20).all()
        return tweets
    except Exception as e:
        flash(str(e))
        print(str(e))


# register a User if it is not registerd
# def check_user(id):
#     user = User.query.filter_by(id=id).first()
#     if user is None:
#         access_token = session.get('access_token', None)
        
#         if access_token is None:
#             return False
#         else:
#             user = User(id, access_token['oauth_token'], access_token['oauth_token_secret'])
#             db.session.add(user)
#             # commit with the Tweet
#             # db.session.commit()
#     return True


# register a Tweet and add or update a User
def insert_tweet(id, user_id, delete_time):
    access_token = session['access_token']
    if access_token is not None:
        try:
            db.session.execute(upsert_user(
                user_id, access_token['oauth_token'], access_token['oauth_token_secret']
                ))
            # db.session.commit()

            tweet = Tweet(id, user_id, delete_time)
            db.session.add(tweet)
            db.session.commit()
        except Exception as e:
            flash(str(e))
            print(str(e))

# create a statement to upsert
def upsert_user(id, token, token_secret):
    stmt = insert(User).values(id=id, access_token=token, access_token_secret=token_secret)
    return stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={'access_token': token, 'access_token_secret': token_secret}
        )


# get Users from user_ids
def get_user(ids):
    try:
        users = User.query.filter_by(id.in_(ids)).all()
        return users
    except Exception as e:
        flash(str(e))
        print(str(e))


# get Tweets to delete and its Users
def get_tweets_to_delete():
    try:
        dt = datetime.now()
        tweetsWithUsers = db.session.query(Tweet, User.access_token, User.access_token_secret).\
            filter(Tweet.delete_time < dt).join(User, Tweet.user_id==User.id).all()

        return tweetsWithUsers
    except Exception as e:
        print(str(e))


# delete Tweets
def delete_tweets(ids):
    try:
        res = db.session.query(Tweet).filter(Tweet.id.in_(ids)).delete()
        db.session.commit()
        return res
    except Exception as e:
        print(str(e))


# delete registration to cancel
def delete_tweet(id):
    try:
        res = Tweet.query.filter_by(id=id).delete()
        db.session.commit()
        return res
    except Exception as e:
        print(str(e))

# delete Users who have no registered Tweets

