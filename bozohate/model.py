import pandas as pd
from pymongo import MongoClient

db = None


def configure(app):
    global db
    db = MongoClient(app.config["MONGO_URI"]).get_database()
    return db


class Tweet:
    def __init__(
        self,
        twitter_id=None,
        created_at=None,
        sentiment_polarity=None,
        sentiment_subjectivity=None,
        original_tweet=None,
        translated_tweet=None,
    ):
        self.twitter_id = twitter_id
        self.created_at = created_at
        self.sentiment_polarity = sentiment_polarity
        self.sentiment_subjectivity = sentiment_subjectivity
        self.original_tweet = original_tweet
        self.translated_tweet = translated_tweet

    def save(self):
        return db.tweet.update(
            {"twitter_id": self.twitter_id},
            {
                "twitter_id": self.twitter_id,
                "created_at": self.created_at,
                "sentiment_polarity": self.sentiment_polarity,
                "sentiment_subjectivity": self.sentiment_subjectivity,
                "original_tweet": self.original_tweet,
                "translated_tweet": self.translated_tweet,
            },
            upsert=True,
        )

    def get(self, query={}):
        return db.tweet.find(query)


class TweetComputed:
    def __init__(
        self,
        total_data=None,
        negative_percent=None,
        negative_value=None,
        date_used=None,
    ):
        self.total_data = total_data
        self.negative_percent = negative_percent
        self.negative_value = negative_value
        self.date_used = date_used

    def save(self):
        return db.tweet_computed.update(
            {"date_used": self.date_used},
            {
                "date_used": self.date_used,
                "last_save": str(pd.Timestamp.now()),
                "total_data": self.total_data,
                "negative_percent": self.negative_percent,
                "negative_value": self.negative_value,
            },
            True,
        )

    def get_all(self):
        return db.tweet_computed.find({}, {"_id": False})
