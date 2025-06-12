# Main script for the function fitting application.
# Orchestrates database setup, data loading, processing, and visualization.

from src.data_processing import load_data
from src.testdata_mapper import select_best_ideal_functions, map_test_data
from src.database import DatabaseManager, TrainingData, IdealFunctions
from src.visualisation import visualise_results
import pandas as pd

# Main function to execute the function fitting workflow
def main():
    try:
        # Initializes database manager and creates tables
        db_manager = DatabaseManager()
        db_manager.create_tables()
        # Loads data from CSV files into the database
        load_data(db_manager)
        # Selects the best ideal functions based on training data
        best_functions = select_best_ideal_functions(db_manager)
        # Maps test data to the best ideal functions
        results = map_test_data(db_manager, best_functions)
        # Creates a database session
        session = db_manager.get_session()
        # Retrieves training and ideal function data as DataFrames
        df_train = pd.read_sql(session.query(TrainingData).statement, session.bind)
        df_ideal = pd.read_sql(session.query(IdealFunctions).statement, session.bind)
        # Converts results to a DataFrame
        df_results = pd.DataFrame(results)
        # Visualizes the results
        visualise_results(df_train, df_ideal, best_functions, df_results)
    except Exception as e:
        print(f"An error occurred in main execution: {e}")
        raise

# Entry point for the script
if __name__ == "__main__":
    main()