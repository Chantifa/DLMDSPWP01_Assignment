from unittest import TestCase
from src.testdata_mapper import map_test_data
from src.database import DatabaseManager
import math


class TestTestDataMapper(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()
        # Here you would need to populate your database with test data or mock data

    def test_map_test_data(self):
        # Mock best_functions with known data
        best_functions = [(1, 1, 0.1), (2, 2, 0.1), (3, 3, 0.1), (4, 4, 0.1)]  # Example data
        results = map_test_data(self.db_manager, best_functions)

        # Check if results are processed
        self.assertTrue(len(results) > 0)
        for result in results:
            if result['ideal_func_no'] != 0:  # If mapped
                self.assertLessEqual(result['delta_y'], math.sqrt(2) * 0.1)  # Check condition for mapping