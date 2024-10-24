import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

# Variable that contains the external_stylesheet to use
external_stylesheets = [dbc.themes.QUARTZ]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet variable to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags, use_pages=True)

# Define the sidebar
sidebar = html.Div(
    [
        # Adjust the heading so it fits in the sidebar properly
        html.H2("Teachers Profile", className="display-4", style={"font-size": "2rem", "color": "#ffffff"}),
        html.H2("Dashboard", className="display-4", style={"font-size": "2rem", "color": "#ffffff"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", id="nav-home", href=dash.page_registry['pages.Home']['path'], active="exact", className="nav-link"),
                dbc.NavLink("Undergraduate", id="nav-undergraduate", href=dash.page_registry['pages.Undergraduate']['path'], active="exact", className="nav-link"),
                dbc.NavLink("Postgraduate", id="nav-postgraduate", href=dash.page_registry['pages.Postgraduate']['path'], active="exact", className="nav-link"),
                dbc.NavLink("Analysis", id="nav-analysis", href=dash.page_registry['pages.Analysis']['path'], active="exact", className="nav-link"),
            ],
            vertical=True,
            pills=True,
            className="flex-column",
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",
        "padding": "1rem 1rem",
        "background-color": "#333333",  # Changed to a darker shade for better contrast
    },
)

# Add a div to wrap the page container and add padding on the left
page_content_style = {
    "margin-left": "270px",
    "margin-right": "20px",
    "padding": "2rem 1rem"
}

app.layout = html.Div([
    # Sidebar
    sidebar,
    # Area where the page content is displayed
    html.Div(id="page-content", style=page_content_style, children=[dash.page_container]),
])

if __name__ == '__main__':
    app.run(debug=True)
