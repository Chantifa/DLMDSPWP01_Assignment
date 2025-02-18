from unittest import TestCase
from src.visualisation import visualize_results
from src.database import DatabaseManager
from unittest.mock import patch

class TestVisualization(TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.session = self.db_manager.get_session()
        # Here you would need to populate your database with test data or mock data

    @patch('src.visualization.show')
    def test_visualize_results(self, mock_show):
        # Mock data for testing
        results = [
            {'x': 1, 'y': 1, 'delta_y': 0.1, 'ideal_func_no': 1},
            {'x': 2, 'y': 2, 'delta_y': 0.2, 'ideal_func_no': 2}
        ]
        visualize_results(results)
        mock_show.assert_called()  # Check if show was called, indicating visualization was attempted