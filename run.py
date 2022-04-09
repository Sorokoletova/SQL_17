from flask import Flask, abort, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

movie_schema = schema.MovieSchema()
movies_schema = schema.MovieSchema(many=True)
genre_schema = schema.GenreSchema()
genres_schema = schema.GenreSchema(many=True)
director_schema = schema.DirectorSchema()
directors_schema = schema.DirectorSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route("/")
class MovieView(Resource):
    def get(self):
        movie_query = db.session.query(schema.Movie)
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movie_query = movie_query.filter(schema.Movie.director_id == director_id)
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movie_query = movie_query.filter(schema.Movie.genre_id == genre_id)
        movies = movie_query.all()
        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(schema.Movie(**movie))
        db.session.commit()

        return "", 201


@movie_ns.route("/<int:nid>")
class MovieView(Resource):
    def get(self, nid):
        movie = schema.Movie.query.get(nid)
        if movie is None:
            abort(404)
        return movie_schema.dump(movie), 200

    def put(self, nid: int):
        movie = db.session.query(schema.Movie).filter(schema.Movie.id == nid).first()
        if movie is None:
            abort(404)
        db.session.query(schema.Movie).filter(schema.Movie.id == nid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, nid: int):
        movie = db.session.query(schema.Movie).filter(schema.Movie.id == nid).first()
        if movie is None:
            abort(404)
        db.session.query(schema.Movie).filter(schema.Movie.id == nid).delete()
        db.session.commit()
        return "", 204


@director_ns.route("/")
class DirectorView(Resource):
    def get(self):
        all_director = schema.Director.query.all()
        return directors_schema.dump(all_director), 200

    def post(self):
        director = director_schema.load(request.json)
        db.session.add(schema.Director(**director))
        db.session.commit()

        return "", 201

@director_ns.route("/<int:nid>")
class DirectorView(Resource):
    def get(self, nid):
        director = schema.Director.query.get(nid)
        if director is None:
            abort(404)
        return director_schema.dump(director), 200

    def put(self, nid: int):
        director = db.session.query(schema.Director).filter(schema.Director.id == nid).first()
        if director is None:
            abort(404)
        db.session.query(schema.Director).filter(schema.Director.id == nid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, nid: int):
        director = db.session.query(schema.Director).filter(schema.Director.id == nid).first()
        if director is None:
            abort(404)
        db.session.query(schema.Director).filter(schema.Director.id == nid).delete()
        db.session.commit()
        return "", 204

@genre_ns.route("/")
class GenreView(Resource):
    def get(self):
        all_genre = schema.Genre.query.all()
        return genres_schema.dump(all_genre), 200


    def post(self):
        genre = genre_schema.load(request.json)
        db.session.add(schema.Genre(**genre))
        db.session.commit()

        return "", 201


@genre_ns.route("/<int:nid>")
class GenreView(Resource):
    def get(self, nid):
        genre = schema.Genre.query.get(nid)
        if genre is None:
            abort(404)
        return genre_schema.dump(genre), 200

    def put(self, nid: int):
        genre = db.session.query(schema.Genre).filter(schema.Genre.id == nid).first()
        if genre is None:
            abort(404)
        db.session.query(schema.Genre).filter(schema.Genre.id == nid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, nid: int):
        genre = db.session.query(schema.Genre).filter(schema.Genre.id == nid).first()
        if genre is None:
            abort(404)
        db.session.query(schema.Genre).filter(schema.Genre.id == nid).delete()
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run()
