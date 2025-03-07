import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.database import TestData, IdealFunctions, TrainingData, Base


def load_data(db_manager):
    # Clear tables before insertion
    with db_manager.engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS training_data"))
        connection.execute(text("DROP TABLE IF EXISTS ideal_functions"))
        connection.execute(text("DROP TABLE IF EXISTS test_data"))
        connection.commit()
    Base.metadata.create_all(db_manager.engine)

    session = db_manager.Session()

    try:
        train_df = pd.read_csv(r'C:\Users\X\PycharmProjects\DLMDSPWP01_Assignment\data\train.csv')
        print("Train Columns:", train_df.columns.tolist())
        print("Train First row:", train_df.head(1).to_dict())
        print(f"Train rows to insert: {len(train_df)}")
        for index, row in train_df.iterrows():
            session.add(TrainingData(x=row['x'], y1=row['y1'], y2=row['y2'], y3=row['y3'], y4=row['y4']))
        session.commit()
        print(f"TrainingData rows after commit: {session.query(TrainingData).count()}")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError in training_data: {e}")
    except FileNotFoundError:
        print("train.csv not found; skipping TrainingData insertion.")


    try:
        ideal_df = pd.read_csv(r'C:\Users\X\PycharmProjects\DLMDSPWP01_Assignment\data\ideal.csv')
        print("Ideal Columns:", ideal_df.columns.tolist())
        print("Ideal First row:", ideal_df.head(1).to_dict())
        print(f"Ideal rows to insert: {len(ideal_df)}")
        for index, row in ideal_df.iterrows():
            y_columns = {f'y{i}': row[f'y{i}'] for i in range(1, 51)}
            session.add(IdealFunctions(x=row['x'], **y_columns))
        session.commit()
        print(f"IdealFunctions rows after commit: {session.query(IdealFunctions).count()}")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError in ideal_functions: {e}")
    except FileNotFoundError:
        print("ideal.csv not found; skipping IdealFunctions insertion.")

    try:
            test_df = pd.read_csv(r'C:\Users\X\PycharmProjects\DLMDSPWP01_Assignment\data\test.csv')
            print("Test Columns:", test_df.columns.tolist())
            print("Test First row:", test_df.head(1).to_dict())
            print(f"Test rows to insert: {len(test_df)}")

            inserted_count = 0
            for index, row in test_df.iterrows():
                try:
                    session.add(TestData(x=row['x'], y=row['y']))
                    session.flush()  # Flush to test this row immediately
                    inserted_count += 1
                except IntegrityError:
                    session.rollback()  # Rollback only this row
                    print(f"Skipped duplicate x value: {row['x']}")
            session.commit()  # Commit all successful insertions
            print(f"TestData rows after commit: {session.query(TestData).count()} (Inserted: {inserted_count})")
    except FileNotFoundError:
            print("test.csv not found; skipping TestData insertion.")

    session.close()
