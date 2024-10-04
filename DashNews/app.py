import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import redis
import json
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

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

# Function to remove HTML tags from content
def clean_html(raw_html):
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator='\n')  # Replace <br/> tags with line breaks

# Function to format list item data
def format_list_item(item_data):
    # Parse the JSON string into a dictionary
    data_dict = json.loads(item_data)
    
    # Extract relevant fields
    item_time = data_dict.get("time", "N/A")
    item_content = data_dict.get("data", {}).get("content", "")
    item_title = data_dict.get("data", {}).get("title", "Untitled")
    item_source = data_dict.get("data", {}).get("source", "Unknown Source")
    
    # Remove HTML tags from the content
    formatted_content = clean_html(item_content)

    # Format into a card-like HTML structure
    return html.Div([
        html.H4(f"Title: {item_title}"),
        html.P(f"Time: {item_time}"),
        html.P(f"Content:\n{formatted_content}"),  # Display cleaned content
        html.P(f"Source: {item_source}"),
        html.Hr()  # Horizontal line to separate items
    ], style={"border": "1px solid #ddd", "padding": "10px", "margin": "10px 0"})


# Callback to fetch and format data from Redis list
@app.callback(
    Output('redis-list-output', 'children'),
    Input('submit-button', 'n_clicks'),
    [Input('redis-key', 'value')]
)
def get_redis_list_items(n_clicks, key):
    if n_clicks > 0 and redis_client.exists(key):
        # Retrieve all items from the Redis list
        list_items = redis_client.lrange(key, 0, -1)
        # Display formatted list items
        return [format_list_item(item) for item in list_items]
    return "Value: (No data found for the provided key)"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
