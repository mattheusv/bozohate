import tweepy
import pandas as pd

from datetime import date, timedelta
from loguru import logger
from textblob import TextBlob
from textblob.exceptions import NotTranslated
from .model import Tweet, TweetComputed


class UpdateCommand:
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._twitter = tweepy.API(auth)

    def execute(self):
        tweets = self._twitter.search("Bolsonaro")
        logger.info(f"fetched {len(tweets)} new tweets from twitter")
        for tweet in tweets:
            try:
                created_at = pd.to_datetime(tweet.created_at, utc=True).tz_convert(
                    "America/Sao_Paulo"
                )
                frase = TextBlob(tweet.text)
                if frase.detect_language() != "en":
                    traducao = TextBlob(
                        str(frase.translate(from_lang=frase.detect_language(), to="en"))
                    )
                    Tweet(
                        tweet.id,
                        str(created_at),
                        traducao.sentiment[0],
                        traducao.sentiment[1],
                        tweet.text,
                        str(traducao),
                    ).save()
                else:
                    Tweet(
                        str(created_at), frase.sentiment[0], frase.sentiment[1], tweet.text
                    ).save()
            except NotTranslated as e:
                logger.error(f"error to translate tweet: {e}")
        logger.success("finish")


class ComputeCommand:
    def __init__(self):
        pass

    def get_percent(self, value, value_total):
        return float("{0:.2f}".format((value / value_total) * 100))

    def execute(self, days_back):
        df = pd.DataFrame(Tweet().get({"sentiment_polarity": {"$ne": 0}}))
        df["created_at"] = pd.to_datetime(df["created_at"])
        df.set_index("created_at", inplace=True)
        date_used = str(date.today() - timedelta(days_back))
        logger.info(f"date used to compute: {date_used}")
        try:
            df = df[date_used]
            tweet_computed = TweetComputed(
                len(df),
                self.get_percent(len(df[df["sentiment_polarity"] < 0]), len(df)),
                len(df[df["sentiment_polarity"] < 0]),
                date_used,
            )
            tweet_computed.save()
        except Exception as e:
            logger.error(f"error to compute tweets: {e}")
