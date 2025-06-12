# Manages loading of CSV data into the database for the function fitting application.
# Handles training data, ideal functions, and test data using pandas and SQLAlchemy.

import pandas as pd
from src.database import DatabaseManager, TrainingData, IdealFunctions, TestData
import os
from sqlalchemy import text

# Loads CSV data from a specified file and populates the database with it
class CSVLoader:
    def __init__(self, file_path):
        # Constructs the absolute file path relative to the project root
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)

    def load_data(self, session):
        # Reads CSV file into a pandas DataFrame
        df = pd.read_csv(self.file_path)
        print(f"Loading {self.file_path} with {len(df)} rows")
        if 'y1' in df.columns and 'y50' not in df.columns:  # Identifies training data
            original_rows = len(df)
            # Removes duplicate x values, keeping the first occurrence
            df = df.drop_duplicates(subset=['x'], keep='first')
            print(f"Training data: original rows {original_rows}, after dedup {len(df)}")
            # Inserts each row into the TrainingData table
            for _, row in df.iterrows():
                session.add(TrainingData(x=row['x'], y1=row['y1'], y2=row['y2'], y3=row['y3'], y4=row['y4']))
        elif 'y50' in df.columns:  # Identifies ideal functions data
            original_rows = len(df)
            # Removes duplicate x values, keeping the first occurrence
            df = df.drop_duplicates(subset=['x'], keep='first')
            print(f"Ideal functions: original rows {original_rows}, after dedup {len(df)}")
            # Inserts each row into the IdealFunctions table
            for _, row in df.iterrows():
                session.add(IdealFunctions(**{col: row[col] for col in df.columns}))
        else:  # Identifies test data
            original_rows = len(df)
            # Removes duplicate x values, keeping the first occurrence
            df = df.drop_duplicates(subset=['x'], keep='first')
            print(f"Test data: original rows {original_rows}, after dedup {len(df)}")
            # Inserts each row into the TestData table
            for _, row in df.iterrows():
                session.add(TestData(x=row['x'], y=row['y']))

# Loads all CSV files (train, ideal, test) into the database
def load_data(db_manager):
    # Creates a new database session
    session = db_manager.get_session()
    try:
        # Drops existing tables to ensure a clean state
        with db_manager.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS training_data"))
            connection.execute(text("DROP TABLE IF EXISTS ideal_functions"))
            connection.execute(text("DROP TABLE IF EXISTS test_data"))
            connection.commit()
        # Recreates the database tables
        db_manager.create_tables()

        # Loads data from each CSV file
        train_loader = CSVLoader('data/train.csv')
        ideal_loader = CSVLoader('data/ideal.csv')
        test_loader = CSVLoader('data/test.csv')
        train_loader.load_data(session)
        ideal_loader.load_data(session)
        test_loader.load_data(session)
        # Commits all changes to the database
        session.commit()
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        raise
    except Exception as e:
        print(f"Database error: {e}")
        # Rolls back changes on error
        session.rollback()
        raise
    finally:
        # Closes the session
        session.close()