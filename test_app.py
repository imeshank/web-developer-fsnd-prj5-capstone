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
        self.executive_producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiYTZkNzBhMTgyMDA2OWQyYmM0ZCIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA1ODY4NzEsImV4cCI6MTY1MDY3MzI3MSwiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.w--ebO-f32_1PHTIYcEQiF9OkUnw2YKc2GF4FETPSVIfetcDWc0uYIFGxDk0PEjCo9ohHDTGn-2qk533Xs4wlKm_zm4rDedCJlQCsLRjL5IF4RswqLNZkoRusvVjhnzPoX4721QdpS5oBIN5_KsdOHs5j9_KMO0vNZXGiBwPOu9n4ABfhhUrddKYQllX68My8GvEvRsFSK3j2akvja7I4uX4vBZlsvNagMAiXZGueI4C-iOC2ip5rZVRMvbae4ErtVJ3koABMY_EgMipR7uMH3B8qPYM5uMlEIIhw44s2WpI1XE-wRTpzzVnKMj7LYmkKOIGEcl8Dne8SbVF05-JPA'}
        self.casting_assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkEwTUZHWU0wakhoZmpDbDZnd3dGNSJ9.eyJpc3MiOiJodHRwczovL2NpbmVtYXByb2plY3QudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyNWNiOWUwN2QzOThkMDA2Zjk0NmFiNyIsImF1ZCI6ImNpbmVhcGkiLCJpYXQiOjE2NTA1ODcwMjQsImV4cCI6MTY1MDY3MzQyNCwiYXpwIjoiWmJKRXZSZ0RabGNtNndDRFZONEtrc0lDMWJ1Sm1CazgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.uxWrjgplvtkC9P7S9LjBtmFFGtHeXANkd2stFIt_Ww0wP6qCFikaxddrFF0_oi_J666VvABbwuV6PO5gvXpXLWtCVu8u3iKshI7bQfP0wcu-bGXu3tmdd70JSj_4PAkc7wbCH-dg_o_1U4iBgYzHTsJB75NAUTHHgaIKKSUHfCz4EHsJXKQg9SbE2ljtAy1FrrUFD2f-4tqMzyRdpKiq8nRPxy7sCXFxWntqIQ1nKuDaXbcB_YttaWwlcRk0kgy3DL5w46vnGnmNggeeb7hYGyRuq9Jq8Sr5LSYFP_x0Goo5AVkWLZHDOVPHB21tOpWfaCpm1MqaQrOuG4w67tY4dg'}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_function(self):
        res = self.client().get("/")
        data = json.loads(res.data)
        # print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])
        self.assertEqual(data["message"], "Testing Success")

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