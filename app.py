import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

app = Dash(__name__)

# Create a dataframe with RATP Data
df_ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=";")
sort_ratp = df_ratp.sort_values(by=['Trafic'], ascending=False)
top_bar = sort_ratp.groupby('Réseau').head(5)
top_pie = df_ratp.head(20)

# Create a dataframe with IDF Data
df_idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=";")
exploit_counts = df_idf.groupby('exploitant')['nom'].count().reset_index()
stations_counts = df_idf.groupby('ligne')['nom'].count().reset_index()

df_idf[['lat', 'lng']] = df_idf['Geo Point'].str.split(',', expand=True)
df_idf['lat'] = df_idf['lat'].str.strip().astype(float)
df_idf['lng'] = df_idf['lng'].str.strip().astype(float)

# Add the layout to the app
app.layout = (html.Div(children=[
    html.H1("Data visualization with Plotly Dash", style={'text-align': 'center', 'text-decoration': 'underline',
                                                          'font-family': 'cursive'}),
    html.H2("Graphs for RATP dataset", style={'color': '#76448A'}),
    html.H3("TOP 10 stations with the biggest trafic and representation of the trafic per cities (TOP5)",
            style={'text-align': 'center'}),
    dcc.Dropdown(
        id='reseau-filter',
        options=[{'label': category, 'value': category} for category in sort_ratp['Réseau'].unique()],
        value=None,
        placeholder='Select a category'),
    dcc.Graph(
        id='bar-chart1',
        figure=px.bar(top_bar, x='Station', y='Trafic', labels={'Station': 'Station', 'Trafic': 'Trafic'}),
        style={'width': '48%', 'align': 'right', 'display': 'inline-block'},
    ),
    dcc.Graph(
        id='pie-chart',
        figure=px.pie(top_pie, values='Trafic', names='Ville', labels={'Ville': 'Ville'}),
        style={'width': '48%', 'align': 'right', 'display': 'inline-block'},
    ),
    html.Div(children=[
        html.H2("Graphs for IDF dataset", style={'color': '#76448A'}),
        dcc.Dropdown(
            id='exploit-filter',
            options=[{'label': category, 'value': category} for category in df_idf['exploitant'].unique()],
            value=None,
            placeholder='Select a category'),
        html.H3("Number of Stations per exploitant", style={'text-align': 'center'}),
        dcc.Graph(
            id='bar-chart2',
            figure=px.bar(exploit_counts, x='exploitant', y='nom',
                          labels={'exploitant': 'Exploitant', 'nom': 'Number of stations'}),
        ),
        html.H3("Number of Stations per line", style={'text-align': 'center'}),
        dcc.Graph(
            id='bar-chart3',
            figure=px.bar(stations_counts, x='ligne', y='nom',
                          labels={'ligne': 'Line', 'nom': 'Number of stations'}),
        ),
        html.H1("Interactive map", style={'color': '#76448A'}),
        html.H3("All the subway station in paris", style={'text-align': 'center'}),
        html.H6("(Double click on the legend to show/hide an exploitant)", style={'text-align': 'center'}),
        dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
            df_idf,
            lat='lat',
            lon='lng',
            hover_name='nom',
            zoom=9,
            color='exploitant',
            hover_data='ligne',
            labels={'exploitant': 'Exploitants', 'lat': 'Latitude', 'lng': 'Longitude', 'ligne': 'Line'}
        ).update_layout(mapbox_style='open-street-map')),
        html.H2("BILLA PIERRE-ANGE", style={'text-align': 'center'}),
        html.H4("Copyright © 2023, ESME Sudria", style={'text-align': 'center'}),
    ])
]))

##############################################################################################
# First, the 2 callbacks for the 2 RATP charts
##############################################################################################
# Define callback for updating the ratp bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart1', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_bar_chart1(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = top_bar
    else:
        # Filter the df based on selection
        filtered_df = top_bar[top_bar['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')


# Define callback for updating the pie chart based on the category filter
@app.callback(
    dependencies.Output('pie-chart', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_pie_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = top_pie
    else:
        # Filter the df based on selection
        filtered_df = df_ratp[df_ratp['Réseau'] ==
                              category].groupby('Ville').sum().sort_values(by=['Trafic'],
                                                                           ascending=False).head(5).reset_index()
    return px.pie(filtered_df, values='Trafic', names='Ville', labels={'Ville': 'Ville'})


##############################################################################################
# Now, the 2 callbacks for the 2 IDF charts
##############################################################################################
# Define callback for updating the first idf bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart2', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = exploit_counts
    else:
        # Filter the df based on selection
        filtered_df = exploit_counts[exploit_counts['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom',
                  labels={'exploitant': 'Exploitant', 'nom': 'Number of stations'})


# Define callback for updating the second idf bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart3', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = stations_counts
    else:
        # Filter the df based on selection
        filtered_df = df_idf[df_idf['exploitant'] == category].groupby('ligne')['nom'].count().reset_index()

    return px.bar(filtered_df, x='ligne', y='nom',
                  labels={'ligne': 'Line', 'nom': 'Number of stations'})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    #Access it on localhost:8050
