# Visualizes training data, ideal functions, and test data results using Bokeh.
# Creates an interactive plot with toggleable legend for function fitting results.

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

# Generates a Bokeh plot to visualize training data, ideal functions, and test data
def visualise_results(df_train, df_ideal, best_functions, df_results):
    # Defines colors for each training function and corresponding ideal function
    colors = ['blue', 'red', 'green', 'orange']
    # Maps ideal function numbers to colors based on best_functions mapping
    ideal_to_color = {ideal_no: colors[train_no - 1] for train_no, ideal_no, _ in best_functions}
    # Assigns colors to test data points based on their ideal function number, defaulting to gray
    df_results['color'] = df_results['ideal_func_no'].map(ideal_to_color).fillna('gray')
    # Creates a Bokeh figure with specified title and axis labels
    p = figure(title="Function Fitter", x_axis_label='x', y_axis_label='y', width=800, height=600)
    # Plots training data (y1-y4) as solid lines
    for i, color in enumerate(colors, start=1):
        p.line(df_train['x'], df_train[f'y{i}'], line_width=2, color=color, legend_label=f'Training y{i}')
    # Plots corresponding ideal functions as dashed lines
    for (train_no, ideal_no, _), color in zip(best_functions, colors):
        p.line(df_ideal['x'], df_ideal[f'y{ideal_no}'], line_width=2, color=color, line_dash='dashed',
               legend_label=f'Ideal for y{train_no}')
    # Creates a data source for test data points
    source = ColumnDataSource(df_results)
    # Plots test data as scatter points with colors based on ideal function mapping
    p.scatter('x', 'y', source=source, size=8, color='color', alpha=0.6, legend_label='Test Data')
    # Configures legend to be positioned at top-left and allows toggling visibility
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    # Displays the plot
    show(p)