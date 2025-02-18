from unittest import TestCase
from src.data_processing import load_data
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData


class TestDataProcessing(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()

    def test_load_data(self):
        load_data(self.db_manager)
        # Check if data was loaded
        self.assertTrue(self.session.query(TrainingData).count() > 0)
        self.assertTrue(self.session.query(IdealFunctions).count() > 0)
        self.assertTrue(self.session.query(TestData).count() > 0)