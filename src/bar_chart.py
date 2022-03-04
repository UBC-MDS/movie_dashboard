import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("data/processed/clean_df.csv")

for i, movie in enumerate(df['duration'].str.split()):
    df['duration'][i] = int(movie[0])

app = Dash(__name__)
server = app.server 

app.layout = html.Div([
        dbc.Label("Year", html_for="range-slider"),
        dcc.RangeSlider(min(df['release_year']), max(df['release_year']), marks=None, value=[1995, 2020],id='year'),
        dbc.Label("Duration", html_for="range-slider"),
        dcc.RangeSlider(min(df['duration']), max(df['duration']), marks=None, value=[60, 120],id='duration'),
        html.Iframe(
            id='bar',
            style={'border-width': '0', 'width': '100%', 'height': '400px'})])

@app.callback(
    Output('bar', 'srcDoc'),
    Input('year','value'),
    Input('duration','value'))

def plot_altair(year_range, duration_range):
    chart = alt.Chart(df[(df["release_year"] > year_range[0]) & (df["release_year"] < year_range[1]) 
                & (df["duration"] > duration_range[0])
                & (df["duration"] < duration_range[1])],
        title='Which Country Make the Most Movies ?').mark_bar().encode(
    alt.X('country', sort='y', title='Country'),
    alt.Y('count()', title='Number of Movies Produced')
    ).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)