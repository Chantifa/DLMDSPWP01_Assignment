from .database import  TestData, TrainingData, IdealFunctions
import math


def map_test_data(db_manager, best_functions):
    session = db_manager.get_session()
    test_data = session.query(TestData).all()

    for test in test_data:
        for func in best_functions:
            train_func_no, ideal_func_no, max_deviation = func
            train_row = session.query(TrainingData).filter_by(x=test.x).first()
            ideal_row = session.query(IdealFunctions).filter_by(x=test.x).first()

            if train_row and ideal_row:
                train_y = train_row.__dict__[f"y{train_func_no}"]
                ideal_y = ideal_row.__dict__[f"y{ideal_func_no}"]
                deviation = abs(test.y - ideal_y)
                if deviation <= max_deviation * math.sqrt(2):
                    test.delta_y = deviation
                    test.ideal_func_no = ideal_func_no
                    break  # Move to next test point once matched

    session.commit()
    return [{"x": test.x, "y": test.y, "delta_y": test.delta_y, "ideal_func_no": test.ideal_func_no}
            for test in test_data]