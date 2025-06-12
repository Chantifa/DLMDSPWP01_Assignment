# Unit tests for the testdata_mapper module in the function fitting application.
# Verifies the selection of best ideal functions and mapping of test data.

import unittest
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData
from src.testdata_mapper import select_best_ideal_functions, map_test_data
from sqlalchemy import text
import math

# Test case class for testdata_mapper functionality
class TestTestDataMapper(unittest.TestCase):
    def setUp(self):
        # Sets up a test database with sample data for training, ideal functions, and test data
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()

        # Drops and recreates tables to ensure a clean state
        with self.db_manager.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS training_data"))
            connection.execute(text("DROP TABLE IF EXISTS ideal_functions"))
            connection.execute(text("DROP TABLE IF EXISTS test_data"))
            connection.commit()

        self.db_manager.create_tables()

        # Populates sample training data
        training_data = [
            TrainingData(x=1.0, y1=1.0, y2=2.0, y3=3.0, y4=4.0),
            TrainingData(x=2.0, y1=1.1, y2=2.1, y3=3.1, y4=4.1)
        ]
        self.session.add_all(training_data)

        # Populates sample ideal functions with values for all 50 y-columns
        ideal_data = [
            IdealFunctions(
                x=1.0,
                y1=1.05, y2=2.05, y3=3.05, y4=4.05, y5=5.05, y6=6.05, y7=7.05, y8=8.05, y9=9.05,
                y10=10.05, y11=11.05, y12=12.05, y13=13.05, y14=14.05, y15=15.05, y16=16.05, y17=17.05,
                y18=18.05, y19=19.05, y20=20.05, y21=21.05, y22=22.05, y23=23.05, y24=24.05, y25=25.05,
                y26=26.05, y27=27.05, y28=28.05, y29=29.05, y30=30.05, y31=31.05, y32=32.05, y33=33.05,
                y34=34.05, y35=35.05, y36=36.05, y37=37.05, y38=38.05, y39=39.05, y40=40.05, y41=41.05,
                y42=42.05, y43=43.05, y44=44.05, y45=45.05, y46=46.05, y47=47.05, y48=48.05, y49=49.05,
                y50=50.05
            ),
            IdealFunctions(
                x=2.0,
                y1=1.15, y2=2.15, y3=3.15, y4=4.15, y5=5.15, y6=6.15, y7=7.15, y8=8.15, y9=9.15,
                y10=10.15, y11=11.15, y12=12.15, y13=13.15, y14=14.15, y15=15.15, y16=16.15, y17=17.15,
                y18=18.15, y19=19.15, y20=20.15, y21=21.15, y22=22.15, y23=23.15, y24=24.15, y25=25.15,
                y26=26.15, y27=27.15, y28=28.15, y29=29.15, y30=30.15, y31=31.15, y32=32.15, y33=33.15,
                y34=34.15, y35=35.15, y36=36.15, y37=37.15, y38=38.15, y39=39.15, y40=40.15, y41=41.15,
                y42=42.15, y43=43.15, y44=44.15, y45=45.15, y46=46.15, y47=47.15, y48=48.15, y49=49.15,
                y50=50.15
            )
        ]
        self.session.add_all(ideal_data)

        # Populates sample test data
        test_data = [
            TestData(x=1.0, y=1.06),
            TestData(x=2.0, y=2.16)
        ]
        self.session.add_all(test_data)

        self.session.commit()

    def tearDown(self):
        # Cleans up by closing the session and disposing of the engine
        self.session.close()
        self.db_manager.engine.dispose()

    def test_select_best_ideal_functions(self):
        # Tests that select_best_ideal_functions returns correct function mappings
        best_functions = select_best_ideal_functions(self.db_manager)
        self.assertEqual(len(best_functions), 4)
        for func in best_functions:
            train_no, ideal_no, max_dev = func
            self.assertTrue(1 <= train_no <= 4, f"train_no {train_no} out of range")
            self.assertTrue(1 <= ideal_no <= 50, f"ideal_no {ideal_no} out of range")
            self.assertTrue(max_dev >= 0, f"max_dev {max_dev} should be non-negative")
        self.assertEqual(best_functions[0][1], 1)  # Verifies y1 matches ideal y1
        self.assertEqual(best_functions[1][1], 2)  # Verifies y2 matches ideal y2

    def test_map_test_data(self):
        # Tests that map_test_data correctly assigns test points to ideal functions
        best_functions = select_best_ideal_functions(self.db_manager)
        results = map_test_data(self.db_manager, best_functions)
        self.assertEqual(len(results), 2)
        for result in results:
            if result['x'] == 1.0:
                self.assertEqual(result['ideal_func_no'], 1)
                self.assertAlmostEqual(result['delta_y'], 0.01, places=2)
            elif result['x'] == 2.0:
                self.assertEqual(result['ideal_func_no'], 2)
                self.assertAlmostEqual(result['delta_y'], 0.01, places=2)