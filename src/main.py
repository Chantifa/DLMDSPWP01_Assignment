from .database import DatabaseManager
from .data_processing import load_data
from .function_fitter import select_best_functions
from .test_data_mapper import map_test_data
from .visualization import visualize_results

def main():
    db_manager = DatabaseManager()
    load_data(db_manager)
    best_functions = select_best_functions(db_manager)
    results = map_test_data(db_manager, best_functions)
    visualize_results(results)

if __name__ == "__main__":
    main()