# Unit tests for the data processing functionality of the function fitting application.
# Verifies that data loading populates the database tables correctly.

from unittest import TestCase
from src.data_processing import load_data
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData

# Test case class for data processing operations
class TestDataProcessing(TestCase):
    def setUp(self):
        # Initializes the database manager and creates a session before each test
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()

    def tearDown(self):
        # Closes the database session after each test
        self.session.close()

    def test_load_data(self):
        # Loads data into the database using the load_data function
        load_data(self.db_manager)
        # Verifies that the TrainingData table contains records
        self.assertTrue(self.session.query(TrainingData).count() > 0)
        # Verifies that the IdealFunctions table contains records
        self.assertTrue(self.session.query(IdealFunctions).count() > 0)
        # Verifies that the TestData table contains records
        self.assertTrue(self.session.query(TestData).count() > 0)