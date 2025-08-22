import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# ----------------------------
# 1. Load Cleaned Data
# ----------------------------
google_df = pd.read_csv("google_clean.csv")
instagram_df = pd.read_csv("instagram_clean.csv")
twitter_df = pd.read_csv("twitter_clean.csv")

# ----------------------------
# 2. Initialize App
# ----------------------------
app = dash.Dash(__name__)

# ----------------------------
# 3. Create Graphs
# ----------------------------

# Google Graphs (financial-like data)
fig_google_line = px.line(google_df, x=google_df.index, y="Close", title="Google Trends Over Time")
fig_google_bar = px.bar(google_df.head(20), x=google_df.index[:20], y="Close", title="Top 20 Google Search Values")
fig_google_scatter = px.scatter(google_df, x="High", y="Low", title="Google High vs Low")

# Instagram Graphs (social metrics)
fig_insta_line = px.line(instagram_df, x=instagram_df.index, y="Likes", title="Instagram Likes Over Time")
fig_insta_bar = px.bar(instagram_df.head(20), x="Caption", y="Comments", title="Top 20 Posts by Comments")
fig_insta_scatter = px.scatter(instagram_df, x="Follows", y="Profile Visits", title="Followers vs Profile Visits")

# Twitter Graphs (assuming similar structure to Google — else share columns)
if "Close" in twitter_df.columns:
    fig_twitter_line = px.line(twitter_df, x=twitter_df.index, y="Close", title="Twitter Trends Over Time")
    fig_twitter_bar = px.bar(twitter_df.head(20), x=twitter_df.index[:20], y="Close", title="Top 20 Tweets")
    fig_twitter_scatter = px.scatter(twitter_df, x="High", y="Low", title="Twitter High vs Low")
else:
    # fallback if Close not available
    first_num_col = twitter_df.select_dtypes(include="number").columns[0]
    fig_twitter_line = px.line(twitter_df, x=twitter_df.index, y=first_num_col, title=f"Twitter {first_num_col} Over Time")
    fig_twitter_bar = px.bar(twitter_df.head(20), x=twitter_df.index[:20], y=first_num_col, title=f"Top 20 Twitter {first_num_col}")
    fig_twitter_scatter = px.scatter(twitter_df, x=twitter_df.select_dtypes(include="number").columns[1],
                                     y=first_num_col, title="Twitter Scatter Plot")

# Combined Dashboard (Compare Google, Instagram, Twitter)
combined_df = pd.DataFrame({
    "Google": google_df["Close"] if "Close" in google_df.columns else google_df.select_dtypes(include="number").iloc[:,0],
    "Instagram": instagram_df["Likes"],
    "Twitter": twitter_df["Close"] if "Close" in twitter_df.columns else twitter_df.select_dtypes(include="number").iloc[:,0],
})

# Ensure all are numeric (remove text, NaN, etc.)
combined_df = combined_df.apply(pd.to_numeric, errors="coerce")

fig_combined_line = px.line(combined_df, title="Cross-Platform Trends Over Time")


# ----------------------------
# 4. App Layout
# ----------------------------
app.layout = html.Div([
    html.H1("📊 Social Media Trends Dashboard", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label="Google Trends", children=[
            dcc.Graph(figure=fig_google_line),
            dcc.Graph(figure=fig_google_bar),
            dcc.Graph(figure=fig_google_scatter)
        ]),
        dcc.Tab(label="Instagram", children=[
            dcc.Graph(figure=fig_insta_line),
            dcc.Graph(figure=fig_insta_bar),
            dcc.Graph(figure=fig_insta_scatter)
        ]),
        dcc.Tab(label="Twitter", children=[
            dcc.Graph(figure=fig_twitter_line),
            dcc.Graph(figure=fig_twitter_bar),
            dcc.Graph(figure=fig_twitter_scatter)
        ]),
        dcc.Tab(label="Combined", children=[
            dcc.Graph(figure=fig_combined_line)
        ])
    ])
])

# ----------------------------
# 5. Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
