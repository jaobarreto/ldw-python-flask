from flask_restful import Resource
from flask import make_response, request, jsonify
from api import api
from ..schemas import movie_schema
from ..models import movie_model
from ..services import movie_service
from bson import ObjectId


class MovieList(Resource):
    def get(self):
        # Obtém todos os filmes do serviço
        movies = movie_service.get_movies()

        # Converte _id para string antes de serializar
        for movie in movies:
            movie['_id'] = str(movie['_id'])

        # Serializa os filmes
        mv = movie_schema.MovieSchema(many=True)
        result = mv.dump(movies)

        return make_response(jsonify(result), 200)

    def post(self):
        mv = movie_schema.MovieSchema()
        errors = mv.validate(request.json)
        if errors:
            return make_response(jsonify(errors), 400)

        # Cria objeto do modelo
        new_movie = movie_model.Movie(
            title=request.json['title'],
            description=request.json['description'],
            year=request.json['year']
        )

        # Salva no banco
        saved_movie = movie_service.add_movie(new_movie)

        # Converte _id para string
        saved_movie['_id'] = str(saved_movie['_id'])

        # Serializa e retorna
        result = mv.dump(saved_movie)
        return make_response(jsonify(result), 201)


# Registra a rota
api.add_resource(MovieList, '/movies')
