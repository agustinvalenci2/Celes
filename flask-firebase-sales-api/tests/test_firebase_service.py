from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.services.firebase_service import FirebaseService

class TestFirebaseService(TestCase):

    @patch('src.services.firebase_service.firestore')
    def test_get_sales_by_employee(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'employee_id': 'emp1', 'amount': 100}),
            MagicMock(to_dict=lambda: {'employee_id': 'emp1', 'amount': 200}),
        ]

        service = FirebaseService()
        result = service.get_sales_by_employee('emp1', '2023-01-01', '2023-01-31')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['amount'], 100)
        self.assertEqual(result[1]['amount'], 200)

    @patch('src.services.firebase_service.firestore')
    def test_get_sales_by_product(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'product_id': 'prod1', 'amount': 150}),
            MagicMock(to_dict=lambda: {'product_id': 'prod1', 'amount': 250}),
        ]

        service = FirebaseService()
        result = service.get_sales_by_product('prod1', '2023-01-01', '2023-01-31')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['amount'], 150)
        self.assertEqual(result[1]['amount'], 250)

    @patch('src.services.firebase_service.firestore')
    def test_get_sales_by_store(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'store_id': 'store1', 'amount': 300}),
            MagicMock(to_dict=lambda: {'store_id': 'store1', 'amount': 400}),
        ]

        service = FirebaseService()
        result = service.get_sales_by_store('store1', '2023-01-01', '2023-01-31')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['amount'], 300)
        self.assertEqual(result[1]['amount'], 400)

    @patch('src.services.firebase_service.firestore')
    def test_get_total_and_average_sales_by_store(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'store_id': 'store1', 'amount': 300}),
            MagicMock(to_dict=lambda: {'store_id': 'store1', 'amount': 700}),
        ]

        service = FirebaseService()
        total, average = service.get_total_and_average_sales_by_store('store1', '2023-01-01', '2023-01-31')

        self.assertEqual(total, 1000)
        self.assertEqual(average, 500)

    @patch('src.services.firebase_service.firestore')
    def test_get_total_and_average_sales_by_product(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'product_id': 'prod1', 'amount': 150}),
            MagicMock(to_dict=lambda: {'product_id': 'prod1', 'amount': 350}),
        ]

        service = FirebaseService()
        total, average = service.get_total_and_average_sales_by_product('prod1', '2023-01-01', '2023-01-31')

        self.assertEqual(total, 500)
        self.assertEqual(average, 250)

    @patch('src.services.firebase_service.firestore')
    def test_get_total_and_average_sales_by_employee(self, mock_firestore):
        mock_sales_collection = MagicMock()
        mock_firestore.client.return_value.collection.return_value = mock_sales_collection
        mock_sales_collection.where.return_value.stream.return_value = [
            MagicMock(to_dict=lambda: {'employee_id': 'emp1', 'amount': 100}),
            MagicMock(to_dict=lambda: {'employee_id': 'emp1', 'amount': 300}),
        ]

        service = FirebaseService()
        total, average = service.get_total_and_average_sales_by_employee('emp1', '2023-01-01', '2023-01-31')

        self.assertEqual(total, 400)
        self.assertEqual(average, 200)