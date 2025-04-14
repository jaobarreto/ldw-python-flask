from api import app, mongo
from api.models.movie_model import Movie
from api.services import movie_service

if __name__ == "__main__":

    with app.app_context():
        if 'movies' not in mongo.db.list_collections_names():
            movie = Movie(
                title='',
                description='',
                year=''

            )
    app.run(host="localhost", port=4000, debug=True)
