from server.api.api_server import api_server
from flask_restx import Resource, Api

app_api = Api(api_server)


@api_server.route('/app_test')
def get():
    return 'hello world'
