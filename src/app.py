from flask import Flask, Blueprint
from src.api.stream.twitter.twitter_trends import MyStreamListener
from src.api.timeline.crypto.crypto_endpoint import ns as graph_namespace
from src.api.restplus import api
from src import settings
from apscheduler.schedulers.background import BackgroundScheduler
import src.crypto_data as crypto
import tweepy


sched = BackgroundScheduler()


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(graph_namespace)
    flask_app.register_blueprint(blueprint)





@sched.scheduled_job(trigger='cron', hour='9', minute='00')
def refresh_crypto_data():
    crypto.create_cryptto_folder_if_not_exist()
    crypto.save_alphavantage_digital_currency_daily('BCH')
    crypto.save_alphavantage_digital_currency_daily('DASH')
    crypto.save_alphavantage_digital_currency_daily('ETH')
    crypto.save_alphavantage_digital_currency_daily('LTC')
    crypto.save_alphavantage_digital_currency_daily('XMR')


app = Flask(__name__)
sched.start()
initialize_app(app)
refresh_crypto_data()
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())


# This is to satisfy GKE healthcheck ingress
@app.route("/")
def health_check():
    return "OK"


if __name__ == "__main__":
    app.run(debug=settings.FLASK_DEBUG)
