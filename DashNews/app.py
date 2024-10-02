import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import redis

# Connect to local Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Plotly Dash with Redis"),
    html.Div("Enter Redis List Key:"),
    dcc.Input(id='redis-key', value='news:Story:ALL', type='text'),
    html.Button('Get List Items', id='submit-button', n_clicks=0),
    html.Div(id='redis-list-output')
])

# Callback to fetch data from Redis list
@app.callback(
    Output('redis-list-output', 'children'),
    Input('submit-button', 'n_clicks'),
    [Input('redis-key', 'value')]
)
def get_redis_list_items(n_clicks, key):
    if n_clicks > 0 and redis_client.exists(key):
        # Retrieve all items from the Redis list
        list_items = redis_client.lrange(key, 0, -1)
        return html.Ul([html.Li(item) for item in list_items])  # Display list items
    return "Value: (No data found for the provided key)"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
