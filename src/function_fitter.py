import numpy as np
from .database import TrainingData, IdealFunctions

def least_squares_residual(train_y, ideal_y):
    return np.sum((train_y - ideal_y) ** 2)


def select_best_functions(db_manager):
    session = db_manager.get_session()
    train_data = session.query(TrainingData).all()
    ideal_data = session.query(IdealFunctions).all()

    residuals = []
    for i in range(1, 5):
        train_y = np.array([d.__dict__[f"y{i}"] for d in train_data])
        for j in range(1, 51):
            ideal_y = np.array([d.__dict__[f"y{j}"] for d in ideal_data])
            residuals.append((i, j, least_squares_residual(train_y, ideal_y)))

    residuals.sort(key=lambda x: x[2])
    return residuals[:4]  # Return the 4 best fits