from src.data_processing import load_data
from src.testdata_mapper import select_best_ideal_functions, map_test_data
from src.database import DatabaseManager, TrainingData, IdealFunctions
from src.visualisation import visualise_results
import pandas as pd

def main():
    try:
        db_manager = DatabaseManager()
        db_manager.create_tables()
        load_data(db_manager)
        best_functions = select_best_ideal_functions(db_manager)
        results = map_test_data(db_manager, best_functions)
        session = db_manager.get_session()
        df_train = pd.read_sql(session.query(TrainingData).statement, session.bind)
        df_ideal = pd.read_sql(session.query(IdealFunctions).statement, session.bind)
        df_results = pd.DataFrame(results)
        visualise_results(df_train, df_ideal, best_functions, df_results)
    except Exception as e:
        print(f"An error occurred in main execution: {e}")
        raise

if __name__ == "__main__":
    main()