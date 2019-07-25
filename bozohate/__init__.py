import sys
import click
from decouple import config
from flask import Flask
from loguru import logger

from .commands import ComputeCommand, UpdateCommand
from .model import configure as config_db
from .view import index, tweet_computed_api

FORMAT_LOGGER = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>"


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = config("SECRET_KEY")
    app.config["MONGO_URI"] = config("MONGO_URI")
    app.config["DEBUG"] = config("FLASK_DEBUG", cast=bool)
    app.config["CONSUMER_KEY"] = config("CONSUMER_KEY")
    app.config["CONSUMER_SECRET"] = config("CONSUMER_SECRET")
    app.config["ACCESS_TOKEN"] = config("ACCESS_TOKEN")
    app.config["ACCESS_TOKEN_SECRET"] = config("ACCESS_TOKEN_SECRET")

    app.db = config_db(app)

    logger.remove()
    logger.add(sys.stdout, level="INFO", format=FORMAT_LOGGER, colorize=True)
    logger.add("bozohate_{time:YYYY-MM-DD}.log", level="ERROR", rotation="5 MB")

    @app.cli.command(help="Get data from twitter")
    def update():
        UpdateCommand(
            app.config["CONSUMER_KEY"],
            app.config["CONSUMER_SECRET"],
            app.config["ACCESS_TOKEN"],
            app.config["ACCESS_TOKEN_SECRET"],
        ).execute()

    @app.cli.command(help="Compute data from database")
    @click.argument("days_back", default=0)
    def compute(days_back):
        ComputeCommand().execute(days_back)

    @app.route("/api/tweet/computed")
    def tweet_computed_route():
        return tweet_computed_api()

    @app.route("/")
    def index_route():
        return index()

    return app
