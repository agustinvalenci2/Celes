from flask import json
from flask_testing import TestCase
from src.app import app


class TestAuthRoutes(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_login_success(self):
        response = self.client.post(
            "/auth/login", json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_failure(self):
        response = self.client.post(
            "/auth/login", json={"username": "wronguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json)

    def test_token_required(self):
        response = self.client.get("/protected-route")
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json)

    def test_token_success(self):
        login_response = self.client.post(
            "/auth/login", json={"username": "testuser", "password": "testpassword"}
        )
        token = login_response.json["token"]
        response = self.client.get(
            "/protected-route", headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json)
