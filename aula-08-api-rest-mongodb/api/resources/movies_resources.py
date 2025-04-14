from flask_restful import Resource, reqparse
from api import api

class MovieList(Resource):
    def get(self):
        return "olá mundo!"
    
    #def post():
   
api.add_resource(MovieList, '/movies')