import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CinemaTestCase(unittest.TestCase):
    """This class represents the cinema test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {"name": "test_movie", "genre": "fairy tale"}
        self.new_movie_without_name = {"genre": "comedy"}
        self.update_movie = {"genre": "test_genre"}
        self.new_actor = {
            "name": "Shala",
            "experience_level": "4",
            "gender": "female",
            "age": "30"}
        self.update_movie_id = '1'
        self.delete_movie_id = '1'
        # JWT token for executive producer
        self.executive_producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiYTZkNzBhMTgyMDA2OWQyYmM0ZCIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA3NzAwODYsImV4cCI6MTY1MDg1NjQ4NiwiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.A-WcMFg7vpM2dMNC6zl8yYZwfbeC1ked8y8VQF40lV3TXnqnKQoyS6Sz5YYple73cOIqmvIMBy46HZz7wlfErXT8rhsTUcNwpeMjbrGlXQhW4j66OYlPSOc40xjETI1OdDCmwS-9z-HkUN-VqeK9nl0YGkzeHH2_NPelrqR6CD531UmQFiyaf1mJYRYLMN3cUIeD3EcfGEEm_d50z_xkCUbYQ-vFIuKjqAardpYipTsDyfH5fUI3qH2AKLKj04UTpTz6khmmGE-KDAWeM3aYmS7v9yUCBnxB1TLv8JJCpD6Y4dDp0nTNKglEGF53yPQ-q5h13R7bf0pVcrp2bqnzHQ'}
        # JWT token for casting assistant
        self.casting_assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiOWUwN2QzOThkMDA2Zjk0NmFiNyIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA3NzAxOTEsImV4cCI6MTY1MDg1NjU5MSwiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.kiwCA2seGQEyPbl0X4wDMuxjXDlJ57a2VP7_0fiYc5JtJxfVvkzneQDgy6N5gv2qDQvWcjkzppSLYlXclAY7mTrobADy0BizA_nneRqtv_cjHbIX1A-ijfIX3Wvly4uL4__XPqZwQ_hpNTfXq-kD90kdT5_R90n9q56KRL27rXxU7JbbB_iB_r8JXcEnDJ8VnTxNCH4ghTHBGAu1ACiSzrrsKXdOzKecldVjuxBcH373qC09M6J6BZUvJBnsz2LF0itiFFs4KWqrLQGyhIjaAvs_j_mutTNAQOO7d-LVc51kw78AdfHPyobJ6WlaV5B50cIxiviG4ADDvCKVwPoCdw'}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_app(self):
        res = self.client().get("/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])
        self.assertEqual(data["message"], "Applicaion is up and running")

    def test_app_fail(self):
        res = self.client().get("/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    # -- Testing all API end points as executive_producer as he has full permission to access the API --#

    def test_get_movies(self):
        res = self.client().get("/movies", headers=self.executive_producer_header)
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_get_movies_with_invalid_name(self):
        res = self.client().get("/moviess", headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    def test_get_actors(self):
        res = self.client().get("/actors", headers=self.executive_producer_header)
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_get_actors_with_invalid_parameter(self):
        res = self.client().get("/actors/4", headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    def test_post_new_movie(self):
        movie_count_before = Movie.query.count()
        res = self.client().post("/movies", json=self.new_movie, headers=self.executive_producer_header)
        data = json.loads(res.data)
        movie_count_after = Movie.query.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        self.assertEqual(movie_count_after-movie_count_before, 1)

    def test_422_movie_creation_without_name(self):
        res = self.client().post("/movies", json=self.new_movie_without_name, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_post_new_actor(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_404_if_actor_creation_not_found(self):
        res = self.client().post("/actorss", json=self.new_actor, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_editing_movie_genre(self):
        res = self.client().patch("/movies/"+self.update_movie_id, json=self.update_movie, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_editing_movie_without_body(self):
        res = self.client().patch("/movies/1", headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_movie(self):
        res = self.client().delete("/movies/"+self.delete_movie_id, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], int(self.delete_movie_id))

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete("/movies/1000", headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # -- casting_assistant has only permission to view actors and movies --

    def test_assistant_permission_to_get_movies(self):
        res = self.client().get("/movies", headers=self.casting_assistant_header)
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_assistant_permission_to_get_actors(self):
        res = self.client().get("/actors", headers=self.casting_assistant_header)
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_assistant_permission_to_add_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_assistant_permission_to_delete_movie(self):
        res = self.client().delete("/movies/"+self.delete_movie_id, headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
