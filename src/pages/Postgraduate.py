from dash import html, register_page, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
# Import the necessary module or file
from figures.figure_postgraduate import bar_ethnicity, line_chart

# register the page in the app
register_page(__name__, name="Undergraduate", title="Undergraduate", path="/Postgraduate")

# Define the layout of the page
# Variables that define the rows and their contents

bar_p = bar_ethnicity(201718)
line_p = line_chart('Awarded QTS')

# Dropdown for selecting the time period of bar chart
time_period_dropdown_p = dcc.Dropdown(
    id='time_period_dropdown_p',
    options=[
        {'label': '2017/18', 'value': 201718},
        {'label': '2018/19', 'value': 201819},
        {'label': '2019/20', 'value': 201920},
        {'label': '2020/21', 'value': 202021},
        {'label': '2021/22', 'value': 202122},
    ],
    value=201718,  # default value
    clearable=False,

    # style the dropdown
    style={'backgroundColor': '#CCCCCC', 'color': '#000000', 'borderRadius': '4px'}
)

# Dropdown for selecting the feature to compare
line_chart_dropdown_p = dcc.Dropdown(
    id='line_chart_dropdown_p',
    options=[
        {'label': 'Awarded QTS', 'value': 'Awarded QTS'},
        {'label': 'Not Awarded QTS', 'value': 'Not awarded QTS'},
        {'label': 'Employed', 'value': 'Teaching in a state-funded school'},
    ],
    value='Awarded QTS',  # default value
    clearable=False,
    # style the dropdown
    style={'backgroundColor': '#CCCCCC', 'color': '#000000', 'borderRadius': '4px'}
)

row_one = dbc.Row([
    dbc.Col([html.H1("Postgraduate Teachers"), html.P("This page displays the"
    f" distribution of postgraduate teachers by ethnicity and the distribution"
    f" of awarded QTS among different time periods.")],
            width=12),
])

# Row with the dropdown
row_two = dbc.Row([
    dbc.Col(children=[time_period_dropdown_p], 
            width=12),
])

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="bar_p", figure=bar_p),
    ], width=12),
])

row_four = dbc.Row([dbc.Col(html.P(""),
                            width=12),])

# Row with the dropdown
row_five = dbc.Row([
    dbc.Col(children=[
        line_chart_dropdown_p,
    ], width=12),
])

row_six = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line_p", figure=line_p),
    ], width=12),
])

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
    row_five,
    row_six,
])


# Define the callback for the bar chart
@callback(
    Output(component_id='bar_p', component_property='figure'),
    Input(component_id='time_period_dropdown_p', component_property='value')
)
def update_bar_chart(time_period):
    figure = bar_ethnicity(time_period)
    return figure


@callback(
    Output(component_id='line_p', component_property='figure'),
    Input(component_id='line_chart_dropdown_p', component_property='value')
)
def update_line_chart(feature):
    figure = line_chart(feature)
    return figure
