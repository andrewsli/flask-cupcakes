from app import app
from models import db, connect_db, Cupcake, DEFAULT_IMAGE
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        self.cupcake = Cupcake(
            flavor='testing', size='small', rating=10)
        db.session.add(self.cupcake)
        db.session.commit()

    def test_all_cupcakes(self):
        """GET /cupcakes should show all cupcakes"""
        response = self.client.get("/cupcakes")
        response_data = response.json["response"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, [{
            "flavor": "testing",
            "size": "small",
            "rating": 10.0,
            "image": DEFAULT_IMAGE,
            "id": response_data[0]["id"]
        }])

    def test_get_single_cupcake(self):
        """GET /cupcakes/<cupcake_id> should show specified cupcake"""
        response = self.client.get(f"/cupcakes/{self.cupcake.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["response"], {
            "flavor": "testing",
            "size": "small",
            "rating": 10,
            "image": DEFAULT_IMAGE,
            "id": response.json["response"]["id"]
        })

    def test_create_cupcake(self):
        """POST to /cupcakes should create cupcake, add it to database,
        and show created cupcake"""
        response = self.client.post(
            "/cupcakes", json={
                "flavor": "testing2",
                "size": "medium",
                "rating": 11,
                "image": '',
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["response"], {
            "flavor": "testing2",
            "size": "medium",
            "rating": 11,
            "image": DEFAULT_IMAGE,
            "id": response.json["response"]["id"]
        })
        self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """PATCH to /cupcakes should update cupcake,
        and show updated cupcake"""
        response = self.client.patch(
            f"/cupcakes/{self.cupcake.id}", json={
                "flavor": "testing3",
                "size": "small",
                "rating": 2,
                "image": DEFAULT_IMAGE,
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["response"], {
                "flavor": "testing3",
                "size": "small",
                "rating": 2,
                "image": DEFAULT_IMAGE,
                "id": response.json["response"]["id"],
            })
        self.assertEqual(Cupcake.query.count(), 1)

    def test_delete_cupcake(self):
        """DELETE to /cupcake/<cupcake_id> should delete cupcake"""
        response = self.client.delete(
            f"/cupcakes/{self.cupcake.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cupcake.query.count(), 0)
