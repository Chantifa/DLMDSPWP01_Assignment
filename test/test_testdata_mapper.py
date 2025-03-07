from unittest import TestCase
from src.testdata_mapper import map_test_data
from src.data_processing import load_data  # Import load_data
from src.database import DatabaseManager
import math

class TestDataMapper(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()
        # Populate the database with test data
        load_data(self.db_manager)  # Ensure tables are populated

    def test_map_test_data(self):
        best_functions = [(1, 1, 0.1), (2, 2, 0.1), (3, 3, 0.1), (4, 4, 0.1)]
        results = map_test_data(self.db_manager, best_functions)

        self.assertTrue(len(results) > 0)
        for result in results:
            if result['ideal_func_no'] is not None:  # Check if mapped (None instead of 0)
                self.assertLessEqual(result['delta_y'], math.sqrt(2) * 0.1)