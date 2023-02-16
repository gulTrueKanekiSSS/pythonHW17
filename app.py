# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Movie_scheme(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()



class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Director_scheme(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
class Genre_scheme(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = Movie_scheme()
movies_schema = Movie_scheme(many=True)

director_scheme = Director_scheme()
directors_scheme = Director_scheme(many=True)

genre_scheme = Genre_scheme()
genres_scheme = Genre_scheme(many=True)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genre')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        if director_id:
            try:
                movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()
                return movies_schema.dump(movies)
            except Exception:
                return "", 404
        genre_id = request.args.get("genre_id")
        if genre_id:
            try:
                movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
                return movies_schema.dump(movies)
            except Exception:
                return "These movies don't exist", 404
        else:
            all_movie = db.session.query(Movie).all()
            return movies_schema.dump(all_movie), 200

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404

@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return directors_scheme.dump(directors), 200
@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return genre_scheme.dump(genres)


if __name__ == '__main__':
    app.run(debug=True)
