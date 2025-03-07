from .data_processing import load_data
from .database import Base
from .database import DatabaseManager
from .function_fitter import select_best_functions
from .testdata_mapper import map_test_data
from .visualisation import visualize_results


def main():
    db_manager = DatabaseManager()
    load_data(db_manager)
    best_functions = select_best_functions(db_manager)
    results = map_test_data(db_manager, best_functions)
    visualize_results(results)
    Base.metadata.create_all(db_manager.engine)

if __name__ == "__main__":
    main()