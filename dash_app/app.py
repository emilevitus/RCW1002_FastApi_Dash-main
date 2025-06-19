import dash
from dash import html, dcc
EXTERNAL_API_URL = 'http://localhost:8000/info'
# info = 'http://localhost:8000/info' 
app = dash.Dash(__name__, requests_pathname_prefix='/dashboard/')
server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.A('Home', href='/'),
        html.H2("Bienvenue sur la page de login"),
        html.Div([
            # html.H3("Aujourd'hui est :"+ info.date +" et maintenant il est :"+info.time),
            # html.P("Information de Météo"),
            # html.P("Ville :"+info.city),
            # html.P("Température :"+info.weather),
            # html.P("Description :"+ info.description)
        ], className="info-box", style={"border": "1px solid #ccc", "padding": "10px", "marginTop": "10px"})
    ], style={'marginTop': 20}),
    
    dcc.Graph(
        id="exmpl_1",
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [6, 9, 4], "type": "bar", "name": "Example 1"},
                {"x": [7, 2, 5], "y": [3, 7, 1], "type": "bar", "name": "Example 2"}
            ]
        }
    )
])
