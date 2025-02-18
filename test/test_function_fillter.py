from unittest import TestCase
from src.function_fitter import select_best_functions, least_squares_residual
from src.database import DatabaseManager
import numpy as np

class TestFunctionFitter(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()
        # Here you would need to populate your database with test data or mock data

    def test_least_squares_residual(self):
        train_y = np.array([1, 2, 3])
        ideal_y = np.array([1, 2, 3])
        residual = least_squares_residual(train_y, ideal_y)
        self.assertEqual(residual, 0)

    def test_select_best_functions(self):
        best_functions = select_best_functions(self.db_manager)
        self.assertEqual(len(best_functions), 4)  # Check if 4 functions are returned
        # Here you would add more checks based on your data and selection criteria