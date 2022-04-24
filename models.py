import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie = Movie(
        name='movie1',
        genre='comedy'
    )
    movie.insert()
    actor = Actor(
        name="Lisa",
        experience_level="3",
        gender="female",
        age=25
    )
    actor.insert()


"""
Movie
"""


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    genre = db.Column(String)

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'genre': self.genre
        }

    '''
    insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
Actor
"""


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    experience_level = db.Column(String)
    gender = db.Column(String)
    age = db.Column(Integer)

    def format(self):
        return{
            'name': self.name,
            'id': self.id,
            'experience_level': self.experience_level,
            'gender': self.gender,
            'age': self.age
        }

    '''
    insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()
