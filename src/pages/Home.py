from dash import html, register_page, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from figures.figure_home import pie_chart_total, pie_chart_age

# register the page in the app
register_page(__name__, name="Home", title="Home", path="/")

# Define the layout of the page
pie_chart_t = pie_chart_total(201718)
pie_chart_a = pie_chart_age(201718, ['Undergraduate', 'Postgraduate'])

# Dropdown for selecting the time period of home page
time_period_dropdown_h = dcc.Dropdown(
    id='time_period_dropdown_h',
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
    style={'backgroundColor': '#FFFFFF', 'color': '#000000', 'borderRadius': '4px'}
)

# Dropdown for selecting the time period of age distribution
time_period_dropdown_a = dcc.Dropdown(
    id='time_period_dropdown_a',
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
    style={'backgroundColor': '#FFFFFF', 'color': '#000000', 'borderRadius': '4px'}
)

# Checklist for selecting the course levels
checklist_a = dbc.Checklist(
    options=[
        {"label": "Undergraduate", "value": "Undergraduate"},
        {"label": "Postgraduate", "value": "Postgraduate"},
    ],
    value=["Undergraduate"],
    id="checklist_a",
    inline=True,
)


row_one = dbc.Row([
    dbc.Col([html.H1("Home"), html.P("Welcome to the Home page of Teacher"
    f" Proflie Dashboard! This dashboard provides National and provider-level"
    f" information about the outcomes for teacher trainees in England in the"
    f" academic year from 2017/18 to 2021/22. This page displays the"
    f" distribution of undergraduate and postgraduate teachers and the "
    f" distribution of age groups among different time periods. Select a"
    f" time period from the dropdown to view the distributions.")],
            width=12)])

# Row with the dropdown
row_two = dbc.Row([
    dbc.Col(children=[time_period_dropdown_h],
            width=2),
])

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="pie_chart_total", figure=pie_chart_t),
    ], width=12, align='center'),
])

row_four = dbc.Row([
    # First column for the dropdown
    dbc.Col(time_period_dropdown_a, width={'size': 2, 'offset': 0, 'order': 1}),
    # Second column for the checklist
    dbc.Col(checklist_a, width={'size': 2, 'offset': 0, 'order': 2}),
], justify='start')

row_five = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="pie_chart_age", figure=pie_chart_a),
    ], width=12, align='center'),
])

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
layout = dbc.Container([
    row_one,
    row_two,
    # Wrap the graph in a card component for better aesthetics
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(id="pie_chart_total", figure=pie_chart_t),
        ]),
        className="mb-3",
        style={'backgroundColor': '#F0F2F5'}  # Light grey background for the card
    ),
    row_four,
    # Wrap the second graph in a card component
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(id="pie_chart_age", figure=pie_chart_a),
        ]),
        className="mb-3",
        style={'backgroundColor': '#F0F2F5'}  # Light grey background for the card
    ),
], fluid=True)


# Define the callback for the bar chart
@callback(
    Output(component_id='pie_chart_total', component_property='figure'),
    Input(component_id='time_period_dropdown_h', component_property='value')
)
def update_pie_chart_t(time_period):
    figure = pie_chart_total(time_period)
    return figure


@callback(
    Output(component_id='pie_chart_age', component_property='figure'),
    [Input(component_id='time_period_dropdown_a', component_property='value'),
     Input(component_id='checklist_a', component_property='value')]
)
def update_pie_chart_a(time_period, course_levels):
    # Now pass the selected course levels to the pie_chart_age function
    figure = pie_chart_age(time_period, course_levels)
    return figure
