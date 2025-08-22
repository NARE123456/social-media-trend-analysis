import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import random
import time

# Dummy trending data generator
def generate_mock_data():
    platforms = ["Twitter", "Google", "YouTube", "Instagram"]
    categories = ["Entertainment", "Sports", "Politics", "Technology", "Comedy"]
    data = {
        "Platform": [random.choice(platforms) for _ in range(20)],
        "Hashtag": [f"#Trend{i}" for i in range(20)],
        "Category": [random.choice(categories) for _ in range(20)],
        "Mentions": [random.randint(100, 10000) for _ in range(20)]
    }
    return pd.DataFrame(data)

# Initialize Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Real-Time Social Media Trends Dashboard"),
    
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # Update every 10 seconds
        n_intervals=0
    ),
    
    dcc.Graph(id='trend-graph'),
    html.Div(id='top-trends')
])

@app.callback(
    [dash.dependencies.Output('trend-graph', 'figure'),
     dash.dependencies.Output('top-trends', 'children')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    df = generate_mock_data()
    fig = px.bar(df, x="Hashtag", y="Mentions", color="Platform",
                 title="Trending Hashtags Across Platforms")
    top = df.sort_values("Mentions", ascending=False).head(5)
    top_trends = [html.P(f"{row.Hashtag} ({row.Platform}) - {row.Mentions} mentions") for row in top.itertuples()]
    return fig, top_trends

if __name__ == '__main__':
    app.run_server(debug=True)
