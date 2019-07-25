from flask import jsonify, render_template

from .model import TweetComputed


def index():
    return render_template("index.html")


def tweet_computed_api():
    tweet_computed = TweetComputed()
    data_resolve = []
    for tc in tweet_computed.get_all():
        data_resolve.append(tc)
    return jsonify(data_resolve)
