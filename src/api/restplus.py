import logging
from flask_restplus import Api
from src import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Bankify Data Visualization Microservice',
          description='A set of APIs to get your data into graphs')


@api.errorhandler
def default_error_handler(e):
    message = str(e)
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500