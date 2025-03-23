from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

def visualise_results(df_train, df_ideal, best_functions, df_results):
    colors = ['blue', 'red', 'green', 'orange']
    ideal_to_color = {ideal_no: colors[train_no - 1] for train_no, ideal_no, _ in best_functions}
    df_results['color'] = df_results['ideal_func_no'].map(ideal_to_color).fillna('gray')
    p = figure(title="Function Fitter", x_axis_label='x', y_axis_label='y', width=800, height=600)
    for i, color in enumerate(colors, start=1):
        p.line(df_train['x'], df_train[f'y{i}'], line_width=2, color=color, legend_label=f'Training y{i}')
    for (train_no, ideal_no, _), color in zip(best_functions, colors):
        p.line(df_ideal['x'], df_ideal[f'y{ideal_no}'], line_width=2, color=color, line_dash='dashed',
               legend_label=f'Ideal for y{train_no}')
    source = ColumnDataSource(df_results)
    p.scatter('x', 'y', source=source, size=8, color='color', alpha=0.6, legend_label='Test Data')
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    show(p)