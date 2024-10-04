import re
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container([
    html.H1("Regex Editor", className="mt-3"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Regular Expression:"),
            dbc.Input(id="regex-input", type="text", placeholder="Enter your regex pattern here"),
        ], width=6),
        dbc.Col([
            dbc.Label("Test String:"),
            dbc.Input(id="test-string-input", type="text", placeholder="Enter a test string here"),
        ], width=6),
    ], className="mt-3"),
    html.Hr(),
    html.Div(id="regex-result", className="mt-3"),
])

# Define the callback to handle regex testing
@app.callback(
    Output("regex-result", "children"),
    Input("regex-input", "value"),
    Input("test-string-input", "value")
)
def test_regex(regex_pattern, test_string):
    if not regex_pattern:
        return dbc.Alert("Please enter a valid regex pattern.", color="warning")
    
    if not test_string:
        return dbc.Alert("Please enter a test string.", color="warning")
    
    try:
        pattern = re.compile(regex_pattern)
        match = pattern.search(test_string)
        if match:
            return dbc.Alert(f"Match found: '{match.group()}' at position {match.start()} to {match.end()}", color="success")
        else:
            return dbc.Alert("No match found. Please adjust your regex pattern.", color="danger")
    except re.error as e:
        return dbc.Alert(f"Invalid regex pattern: {e}", color="danger")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)