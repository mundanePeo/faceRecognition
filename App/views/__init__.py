from .views_api import faceRecData, faceRec, createdb, deltable

from flask_restful import Api

api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(faceRec, '/faceRec', methods=['POST', 'PUT', 'DELETE'])
api.add_resource(faceRecData, '/faceRecData', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(createdb, '/createdb', methods=['POST', 'GET'])
api.add_resource(deltable, '/deltable', methods=['POST', 'GET'])
