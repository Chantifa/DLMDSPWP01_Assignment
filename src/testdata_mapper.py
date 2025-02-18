from .database import DatabaseManager, TestData, TrainingData, IdealFunctions
import math

def map_test_data(db_manager, best_functions):
    session = db_manager.get_session()
    test_data = session.query(TestData).all()

    for func in best_functions:
        train_func_no, ideal_func_no, max_deviation = func
        for test in test_data:
            train_y = session.query(TrainingData).filter_by(x=test.x).first().__dict__[f"y{train_func_no}"]
            ideal_y = session.query(IdealFunctions).filter_by(x=test.x).first().__dict__[f"y{ideal_func_no}"]
            deviation = abs(test.y - ideal_y)
            if deviation <= max_deviation * math.sqrt(2):
                test.delta_y = deviation
                test.ideal_func_no = ideal_func_no
                session.commit()
                break

    return [{"x": test.x, "y": test.y, "delta_y": test.delta_y, "ideal_func_no": test.ideal_func_no} for test in test_data]