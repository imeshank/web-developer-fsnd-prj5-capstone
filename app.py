import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, db_drop_and_create_all
from auth import AuthError, requires_auth

from flask_migrate import Migrate


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    setup_db(app)
    # db_drop_and_create_all() # if you uncomment this line, it'll create a new database on app refresh. 

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/', methods=['GET'])
    def test():
        return jsonify(
                    {
                        "success": True,
                        "message": "Testing Success"
                    }
            )

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            # fetch all movies in the db
            movie_list = Movie.query.all()
            # convert fetched movie list to data representation
            movies = [movie.format() for movie in movie_list]

            if len(movies) == 0:
                print("movie list is empty")
                abort(404)

            return jsonify(
                    {
                        "success": True,
                        "movies": movies
                    }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                print(e)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            # fetch all actors in the db
            actor_list = Actor.query.all()
            # convert fetched actors list to data representation
            actors = [actor.format() for actor in actor_list]

            if len(actors) == 0:
                print("actors list is empty")
                abort(404)

            return jsonify(
                    {
                        "success": True,
                        "actors": actors
                    }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                print(e)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    # def post_movies(payload):
    def post_movies(payload):
        # get data in the request body
        body = request.get_json()
        new_name = body.get("name", None)
        new_genre = body.get("genre", None)

        if new_name is None:
            abort(422)

        try:
            movie = Movie(name=new_name, genre=new_genre)
            movie.insert()
            return jsonify(
                {
                    "success": True,
                    "movie": [movie.format()]
                }
            )
        except Exception as e:
            print(e)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    # def post_actors(payload):
    def post_actors(payload):
        # get data in the request body
        body = request.get_json()
        new_name = body.get("name", None)
        new_experience_level = body.get("experience_level", None)
        new_gender = body.get("gender", None)
        new_age = body.get("age", None)

        if new_name is None:
            abort(422)

        try:
            actor = Actor(
                name=new_name,
                experience_level=new_experience_level,
                gender=new_gender,
                age=new_age)
            actor.insert()
            return jsonify(
                {
                    "success": True,
                    "actor": [actor.format()]
                }
            )
        except Exception as e:
            print(e)

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    # def update_movie(payload, id):
    def update_movie(payload, id):
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            # fetch the corresponding row from the db according to the given id
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)

            if "name" in body:
                movie.name = body.get("name")
            if "genre" in body:
                movie.genre = body.get("genre")

            movie.update()
            return jsonify(
                {
                    "success": True,
                    "movie": [movie.format()]
                }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                print(e)

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    # def delete_movie(payload, id):
    def delete_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": movie.id
                }
            )
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                print(e)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
