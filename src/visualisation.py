from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from .database import DatabaseManager


def visualize_results(results):
    output_notebook()
    p = figure(title="Function Fit", x_axis_label='X', y_axis_label='Y')

    for result in results:
        if result['ideal_func_no'] != 0:  # If mapped to an ideal function
            p.scatter(result['x'], result['y'], legend_label=f"Test Data - Func {result['ideal_func_no']}", size=5)

    show(p)