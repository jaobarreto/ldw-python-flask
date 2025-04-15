from api import mongo
from ..models import movie_model


def add_movie(movie):
    """
    Adiciona um novo filme ao banco de dados e retorna o documento completo inserido.
    """
    result = mongo.db.movies.insert_one({
        'title': movie.title,
        'description': movie.description,
        'year': movie.year
    })
    new_movie = mongo.db.movies.find_one({'_id': result.inserted_id})
    return new_movie


def get_movies():
    """
    Retorna todos os filmes da coleção como uma lista.
    """
    return list(mongo.db.movies.find())
