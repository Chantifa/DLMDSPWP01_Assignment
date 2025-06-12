# Processes training and ideal function data to select best-fitting functions and maps test data to them.
# Uses pandas for data manipulation and SQLAlchemy for database operations.

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData
import math

# Selects the best ideal functions for each training function based on least sum of squared differences
def select_best_ideal_functions(db_manager):
    try:
        # Creates a database session and loads training and ideal function data into DataFrames
        session = db_manager.get_session()
        df_train = pd.read_sql(session.query(TrainingData).statement, session.bind)
        df_ideal = pd.read_sql(session.query(IdealFunctions).statement, session.bind)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error: {e}")

    # Checks if data is present
    if df_train.empty or df_ideal.empty:
        raise ValueError("Training or ideal data is missing from the database.")

    # Defines required columns for training and ideal data
    required_train_cols = ['x', 'y1', 'y2', 'y3', 'y4']
    required_ideal_cols = ['x'] + [f'y{i}' for i in range(1, 51)]

    # Validates training data columns for presence and numeric type
    for col in required_train_cols:
        if col not in df_train or not pd.api.types.is_numeric_dtype(df_train[col]):
            raise TypeError(f"Training data column '{col}' is missing or not numeric.")

    # Validates ideal data columns for presence and numeric type
    for col in required_ideal_cols:
        if col not in df_ideal or not pd.api.types.is_numeric_dtype(df_ideal[col]):
            raise TypeError(f"Ideal data column '{col}' is missing or not numeric.")

    # Finds the best ideal function for each training function (y1-y4)
    best_functions = []
    for i in range(1, 5):
        yi = f'y{i}'
        sums = {}
        # Calculates sum of squared differences for each ideal function
        for j in range(1, 51):
            yj = f'y{j}'
            sum_sq_diff = ((df_train[yi] - df_ideal[yj]) ** 2).sum()
            sums[j] = sum_sq_diff
        # Selects the ideal function with minimum sum of squared differences
        best_j = min(sums, key=sums.get)
        max_deviation = (df_train[yi] - df_ideal[f'y{best_j}']).abs().max()
        best_functions.append((i, best_j, max_deviation))
    return best_functions

# Maps test data to the best ideal functions based on deviation criteria
def map_test_data(db_manager, best_functions):
    # Retrieves all test data from the database
    session = db_manager.get_session()
    test_data = session.query(TestData).all()

    # Checks if test data is present
    if not test_data:
        raise ValueError("Test data is missing from the database.")

    # Maps each test data point to an ideal function if within deviation threshold
    for test in test_data:
        test.delta_y = None
        test.ideal_func_no = None
        for _, ideal_func_no, max_deviation in best_functions:
            # Finds the corresponding ideal function value for the test x value
            ideal_row = session.query(IdealFunctions).filter_by(x=test.x).first()
            if ideal_row:
                ideal_y = getattr(ideal_row, f"y{ideal_func_no}")
                deviation = abs(test.y - ideal_y)
                # Assigns the ideal function if deviation is within sqrt(2) * max_deviation
                if deviation <= max_deviation * math.sqrt(2):
                    test.delta_y = deviation
                    test.ideal_func_no = ideal_func_no
                    break
    # Commits changes to the database
    session.commit()
    # Returns test data with mapping results
    return [{"x": test.x, "y": test.y, "delta_y": test.delta_y, "ideal_func_no": test.ideal_func_no}
            for test in test_data]