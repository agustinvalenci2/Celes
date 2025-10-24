from flask import json
from flask_testing import TestCase
from src.app import app


class TestSalesRoutes(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_sales_by_employee(self):
        response = self.client.get(
            "/sales/employee/<KeyEmployee>?start_date=<start_date>&end_date=<end_date>"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("sales", json.loads(response.data))

    def test_sales_by_product(self):
        response = self.client.get(
            "/sales/product/<KeyProduct>?start_date=<start_date>&end_date=<end_date>"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("sales", json.loads(response.data))

    def test_sales_by_store(self):
        response = self.client.get(
            "/sales/store/<KeyStore>?start_date=<start_date>&end_date=<end_date>"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("sales", json.loads(response.data))

    def test_total_average_sales_by_store(self):
        response = self.client.get("/sales/store/<KeyStore>/total_average")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", json.loads(response.data))
        self.assertIn("average", json.loads(response.data))

    def test_total_average_sales_by_product(self):
        response = self.client.get("/sales/product/<KeyProduct>/total_average")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", json.loads(response.data))
        self.assertIn("average", json.loads(response.data))

    def test_total_average_sales_by_employee(self):
        response = self.client.get("/sales/employee/<KeyEmployee>/total_average")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", json.loads(response.data))
        self.assertIn("average", json.loads(response.data))
