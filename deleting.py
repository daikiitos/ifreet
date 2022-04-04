import tweeting
import database

def delete():
    tweetsWithUsers = database.get_tweets_to_delete()

    if len(tweetsWithUsers) > 0:
        deleted = tweeting.delete_tweets(tweetsWithUsers)

        # # if deleted is not None and len(deleted) > 0:
        #     #delete Tweets whose tweet has been deleted successfully
        #     database.delete_tweets(deleted)

        # delete Tweets whether deleted successfully or not
        ids = []
        for twu in tweetsWithUsers:
            ids.append(twu.Tweet.id)
        database.delete_tweets(ids)