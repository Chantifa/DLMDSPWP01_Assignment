from unittest import TestCase
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData
from sqlalchemy.exc import SQLAlchemyError
import os

class TestDatabase(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()

    def tearDown(self):
        # Clean up the database after each test
        os.remove('function_fitter.db')

    def test_create_tables(self):
        # Check if tables are created in the database
        tables = self.db_manager.engine.table_names()
        self.assertIn('training_data', tables)
        self.assertIn('ideal_functions', tables)
        self.assertIn('test_data', tables)

    def test_add_data(self):
        # Test adding data to the database
        training = TrainingData(x=1.0, y1=2.0, y2=3.0, y3=4.0, y4=5.0)
        self.session.add(training)
        self.session.commit()
        self.assertEqual(self.session.query(TrainingData).count(), 1)

    def test_exception_handling(self):
        # Test if SQLAlchemyError is raised for invalid operations
        with self.assertRaises(SQLAlchemyError):
            self.session.execute("INSERT INTO non_existent_table (id) VALUES (1)")