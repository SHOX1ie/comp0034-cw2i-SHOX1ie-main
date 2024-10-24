from dash import html, register_page, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from pathlib import Path
import pandas as pd
from figures.figure_analysis import line_chart_analysis

# register the page in the app
register_page(__name__, name="Analysis", title="Analysis", path="/Analysis")

# Extract the data
data_path = Path(__file__).parent.parent.parent.joinpath("data", "df_prepared.csv")

data = pd.read_csv(data_path)

# Define the layout of the page
time_periods = [
    '201718',
    '201819',
    '201920',
    '202021',
    '202122'
]
line_chart_a = line_chart_analysis(data, 'pct_total_age_u25', time_periods)

# Dropdown for selecting the feature to compare
feature_dropdown = dbc.Select(
        id='feature_dropdown',
        options=[
            {'label': 'Age Under 25', 'value': 'pct_total_age_u25'},
            {'label': 'Age 25 and Over', 'value': 'pct_total_age_25andover'},
            {'label': 'Male', 'value': 'pct_total_sex_m'},
            {'label': 'Female', 'value': 'pct_total_sex_f'}
        ],
        value='pct_total_age_u25',  # default value to display
        style={'backgroundColor': '#CCCCCC', 'color': '#000000', 'borderRadius': '4px'}
    )

# RangeSlider for selecting the time period
time_period_slider = dcc.RangeSlider(
    id='time_period_slider',
    min=0,
    max=len(time_periods) - 1,
    value=[0, len(time_periods) - 1],
    marks={i: period for i, period in enumerate(time_periods)},
    step=1,
    className='custom-range-slider'
)

row_one = dbc.Row([
    dbc.Col([html.H1("Data Analysis"), html.P("This page displays the"
            f" comparison of different features of undergraduates and"
        f" postgraduates over time. Select a feature from the dropdown and a"
        f" time period using the slider to view the comparison.")],
            width=12),
])

# Row with the dropdown
row_two = dbc.Row([
    dbc.Col(children=[feature_dropdown],
            width=12),
])

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line_chart_a", figure=line_chart_a),
    ], width=12),
])

row_four = dbc.Row([dbc.Col(html.P(""),
                            width=12),])

# Row with the slider
row_five = dbc.Row([
    dbc.Col(children=[time_period_slider],
            width=12),
])

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
    row_five,
])


# Callback for the line chart and feature dropdown
@callback(
    Output('line_chart_a', 'figure'),
    [Input('feature_dropdown', 'value'),
     Input('time_period_slider', 'value')]
)
def update_line_chart(selected_feature, selected_time_range):
    # Convert slider indices to actual time period values
    selected_time_periods = [time_periods[i]
                             for i in range(selected_time_range[0], selected_time_range[1] + 1)]

    fig = line_chart_analysis(data, selected_feature, selected_time_periods)
    return fig
