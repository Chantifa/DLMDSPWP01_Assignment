import pandas as pd
from .database import TrainingData, IdealFunctions, TestData

def load_data(db_manager):
    session = db_manager.get_session()

    for i in range(1, 5):
        df = pd.read_csv(f'data/training_data_{i}.csv')
        for _, row in df.iterrows():
            session.add(TrainingData(x=row['X'], **{f'y{i}': row['Y']}))

    ideal_df = pd.read_csv('data/ideal_functions.csv')
    for _, row in ideal_df.iterrows():
        session.add(IdealFunctions(x=row['X'], **{f'y{i}': row[f'Y{i}'] for i in range(1, 51)}))

    test_df = pd.read_csv('data/test_data.csv')
    for _, row in test_df.iterrows():
        session.add(TestData(x=row['X'], y=row['Y'], delta_y=0, ideal_func_no=0))

    session.commit()