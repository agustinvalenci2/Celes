from flask import jsonify, request
from src.services.firebase_service import FirebaseService
from src.services.jwt_service import JWTService


class SalesController:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.jwt_service = JWTService()

    def get_sales_by_employee(self, key_employee):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        sales_data = self.firebase_service.get_sales_by_employee(
            key_employee, start_date, end_date
        )
        return jsonify(sales_data)

    def get_sales_by_product(self, key_product):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        sales_data = self.firebase_service.get_sales_by_product(
            key_product, start_date, end_date
        )
        return jsonify(sales_data)

    def get_sales_by_store(self, key_store):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        sales_data = self.firebase_service.get_sales_by_store(
            key_store, start_date, end_date
        )
        return jsonify(sales_data)

    def get_total_average_sales_by_store(self, key_store):
        sales_data = self.firebase_service.get_total_average_sales_by_store(key_store)
        return jsonify(sales_data)

    def get_total_average_sales_by_product(self, key_product):
        sales_data = self.firebase_service.get_total_average_sales_by_product(
            key_product
        )
        return jsonify(sales_data)

    def get_total_average_sales_by_employee(self, key_employee):
        sales_data = self.firebase_service.get_total_average_sales_by_employee(
            key_employee
        )
        return jsonify(sales_data)
