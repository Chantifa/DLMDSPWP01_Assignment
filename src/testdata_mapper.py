import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData
import math

def select_best_ideal_functions(db_manager):
    """Select the best ideal functions for each training function using least squares.

    Args:
        db_manager: DatabaseManager instance.

    Returns:
        list of tuples: Each tuple contains (train_func_no, ideal_func_no, max_deviation).

    Raises:
        RuntimeError: If a database error occurs.
        ValueError: If training or ideal data is missing.
        TypeError: If data columns are not numeric.
    """
    try:
        session = db_manager.get_session()
        df_train = pd.read_sql(session.query(TrainingData).statement, session.bind)
        df_ideal = pd.read_sql(session.query(IdealFunctions).statement, session.bind)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error: {e}")

    if df_train.empty or df_ideal.empty:
        raise ValueError("Training or ideal data is missing from the database.")

    # Verify numeric columns separately for each DataFrame
    required_train_cols = ['x', 'y1', 'y2', 'y3', 'y4']
    required_ideal_cols = ['x'] + [f'y{i}' for i in range(1, 51)]

    # Check training data columns
    for col in required_train_cols:
        if col not in df_train or not pd.api.types.is_numeric_dtype(df_train[col]):
            raise TypeError(f"Training data column '{col}' is missing or not numeric.")

    # Check ideal data columns
    for col in required_ideal_cols:
        if col not in df_ideal or not pd.api.types.is_numeric_dtype(df_ideal[col]):
            raise TypeError(f"Ideal data column '{col}' is missing or not numeric.")

    best_functions = []
    for i in range(1, 5):
        yi = f'y{i}'
        sums = {}
        for j in range(1, 51):
            yj = f'y{j}'
            sum_sq_diff = ((df_train[yi] - df_ideal[yj]) ** 2).sum()
            sums[j] = sum_sq_diff
        best_j = min(sums, key=sums.get)
        max_deviation = (df_train[yi] - df_ideal[f'y{best_j}']).abs().max()
        best_functions.append((i, best_j, max_deviation))
    return best_functions

def map_test_data(db_manager, best_functions):
    """Map test data to the chosen ideal functions based on deviation criteria.

    Args:
        db_manager: DatabaseManager instance.
        best_functions: list of (train_func_no, ideal_func_no, max_deviation).

    Returns:
        list of dicts: Mapped test data with x, y, delta_y, ideal_func_no.

    Raises:
        ValueError: If test data is missing from the database.
    """
    session = db_manager.get_session()
    test_data = session.query(TestData).all()

    if not test_data:
        raise ValueError("Test data is missing from the database.")

    for test in test_data:
        test.delta_y = None
        test.ideal_func_no = None
        for _, ideal_func_no, max_deviation in best_functions:
            ideal_row = session.query(IdealFunctions).filter_by(x=test.x).first()
            if ideal_row:
                ideal_y = getattr(ideal_row, f"y{ideal_func_no}")
                deviation = abs(test.y - ideal_y)
                if deviation <= max_deviation * math.sqrt(2):
                    test.delta_y = deviation
                    test.ideal_func_no = ideal_func_no
                    break
    session.commit()
    return [{"x": test.x, "y": test.y, "delta_y": test.delta_y, "ideal_func_no": test.ideal_func_no}
            for test in test_data]