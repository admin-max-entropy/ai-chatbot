import dash
from dash import dcc, html

dash.register_page(__name__, order=0, path="/")

layout = html.Div(className="row")
