from unittest import TestCase
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
import os
import time

from src.database import DatabaseManager, TrainingData, Base
from sqlalchemy import text

class TestDatabase(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.db_manager = None

    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()

        # Drop and recreate all tables
        with self.db_manager.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS training_data"))
            connection.execute(text("DROP TABLE IF EXISTS ideal_functions"))
            connection.execute(text("DROP TABLE IF EXISTS test_data"))
            connection.commit()
        Base.metadata.create_all(self.db_manager.engine)

    def tearDown(self):
        self.session.close()
        self.db_manager.engine.dispose()

        db_path = 'function_fitter.db'
        if os.path.exists(db_path):
            for _ in range(5):
                try:
                    os.remove(db_path)
                    break
                except PermissionError:
                    time.sleep(0.1)
            else:
                print(f"Warning: Could not remove {db_path} after retries")

    def test_create_tables(self):
        inspector = inspect(self.db_manager.engine)
        tables = inspector.get_table_names()
        self.assertIn('training_data', tables)
        self.assertIn('ideal_functions', tables)
        self.assertIn('test_data', tables)

    def test_add_data(self):
        training = TrainingData(x=1.0, y1=2.0, y2=3.0, y3=4.0, y4=5.0)
        self.session.add(training)
        self.session.commit()
        self.assertEqual(self.session.query(TrainingData).count(), 1)

    def test_exception_handling(self):
        with self.assertRaises(SQLAlchemyError):
            self.session.execute("INSERT INTO non_existent_table (id) VALUES (1)")