# Data Visualization with Plotly Dash

<!-- TOC -->
* [Data Visualization with Plotly Dash](#data-visualization-with-plotly-dash)
  * [About the app](#about-the-app)
  * [About Plotly Dash](#about-plotly-dash)
  * [Installation](#installation)
  * [How to use it ?](#how-to-use-it-)
      * [Full example](#full-example)
  * [Two additional concepts](#two-additional-concepts)
    * [1 - Basics callback](#1---basics-callback)
    * [2 - Advanced visualization - Maps](#2---advanced-visualization---maps)
* [Practice and main app](#practice-and-main-app)
    * [Data](#data)
    * [First step - Create some graph for RATP dataset](#first-step---create-some-graph-for-ratp-dataset)
    * [Second step - Create some graph for IDF dataset](#second-step---create-some-graph-for-idf-dataset)
    * [Third step - Add some global filters](#third-step---add-some-global-filters)
    * [Fourth part - Create an interactive map](#fourth-part---create-an-interactive-map)
    * [Fifth part - Containerize your plotly dash application](#fifth-part---containerize-your-plotly-dash-application)
    * [Last part - Push the app in GitHub](#last-part---push-the-app-in-github)
<!-- TOC -->

## About the app

One good solution for someone coming from the data field is to use a framework 
like Plotly Dash. It allows you to create dynamic and interactive web-based
application using python code. 
Also, it allows you to manipulate the data using pandas which make it a 
good choice for people from the data field.

The goal of the exercise is to :
* Create a web-based dashboard using plotly dash
* Make it ready for distribution with docker
* Manage the code versioning with git (in a good manner)


## About Plotly Dash

Plotly Dash is described by its developers as The original low-code 
framework for rapidly building data apps in Python.
The main advantage of this framework is that you don't have to write
extensive html, css or javascript. In addition, it follows a reactive 
programming paradigm, which basically mean that changes in the user 
interface trigger changes in the data, and changes in the data trigger
changes in the UI.

## Installation

It is very straightforward to install ! 
Simply run `pip install dash` and you're done.

## How to use it ?

Dash come with a set of components that are ready to use.

* html components : Instead of writing HTML or using an HTML templating
engine, you compose your layout using Python with the Dash HTML 
Components module `dash.html`.
* core components : The Dash Core Components module `dash.dcc`
gives you access to many interactive components, including graphs, 
dropdowns, checklists, and sliders.

As previously mentioned, plotly allow you to pass it some data from 
a pandas dataframe, which makes really easy to work with csv data.
If we want to create a bar chart or another figure of the graph
there is a multiple way to do it but the most straightforward is 
with using plotly express api.


#### Full example
Here is an example of the 2 concepts above
```python
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

app = Dash(__name__)

# Create a dataframe with fake data (you can use data from a csv or any source instead...)
df = pd.DataFrame({'Category': ['A', 'B', 'C', 'D'],
                   'Value': [10, 20, 15, 5]})

app.layout = (html.Div(children=[
    html.H1("My first graph"),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(df, x='Category', y='Value')
    )
]))

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Two additional concepts
### 1 - Basics callback
To achieve filtering (with a dropdown, an input value or whatever), 
you'll need to define callback to update the graph. 
Let's use the same input data (category / value df). 
We want to be able to filter for specific category, to do so, we will 
add a dropdown filter :
```python
 dcc.Dropdown(
            id='category-filter',
            options=[{'label': category, 'value': category} for category in df['Category']],
            value=None,
            placeholder='Select a category'
        )
```
Now, we want to update our barchart when a category is selected
in the dropdown -> Let's implement a callback
```python
@app.callback(
    dependencies.Output('bar-chart', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = df
    else:
        # Filter the df based on selection
        filtered_df = df[df['Category'] == category]

    return px.bar(filtered_df, x='Category', y='Value')
```
### 2 - Advanced visualization - Maps
There are a lot of visualization in plotly dash, let's see an example
on how can we draw a map based on some coordinates !

You can do it by using `px.scatter_mapbox()` to generate a map 
figure, you need to specify `lat` & `lon` column name and your dataframe.

Here is an example with a defined dataframe
```python
df = pd.DataFrame({'City': ['Paris', 'New York', 'Los Angeles', 'Tokyo'],
                   'Lat': [48.8566, 40.7128, 34.0522, 35.6895],
                   'Lon': [2.3522, -74.0060, -118.2437, 139.6917],
                   'Value': [10, 20, 15, 5]})

app.layout = html.Div(children=[
    html.H1("My first map", style={'color': '#ADD8E6'}),
    dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
        df, 
        lat='Lat',
        lon='Lon',
        hover_name='City',
        zoom=1
    ).update_layout(mapbox_style='open-street-map'))
])
```
# Practice and main app
### Data
For this exercise, we'll use two input dataset (in csv format).
* One from [RATP](https://data.ratp.fr/explore/dataset/trafic-annuel-entrant-par-station-du-reseau-ferre-2021/export/) 
This dataset represents all the stations managed by 
RATP in "Ile de France" (with each transport mode : subway, train etc...)
and their number of travelers for the year 2021. 
You also have the city they belong to, and the district.
* One from [ile-de-france-mobilités](https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/export/)
This dataset contains all the positions of the stations, 
this time not only for RATP, but also SNCF etc...

### First step - Create some graph for RATP dataset
We create a <u>bar chart</u> that represents the TOP 10 stations with the biggest traffic
and a <u>pie chart</u> that represents trafic per cities. We
organize those two chart on the same row.

### Second step - Create some graph for IDF dataset

Now we create a bar chart that represents the number of stations per exploitant
and a chart that represents the number of stations per line.

Those two steps are done thanks to the technique expressed at the [beginning](#full-example)

### Third step - Add some global filters

Now we need to add some global filter to our dashboard, 
using some dropdown selection filter. referring to the [previous part](#1---basics-callback)
So we are implementing one filter for <u>réseau</u> (field from the RATP dataset)
One filter for <u>exploitant</u> (field from the IDF dataset)

### Fourth part - Create an interactive map

With the technique mentioned [here](#2---advanced-visualization---maps)
we add a Map to your dashboard to visualize the position of the stations.
To get a better visualization of all stations we add some parameters
```color='exploitant'``` ou encore ```hover_data=['mode', 'ligne']``` are used
to get information about the point we are searching on the map.

All the code is on `app.py` and after running the code,
we can access your dashboard at http://127.0.0.1:8050/

### Fifth part - Containerize your plotly dash application

Now that we have our dashboard code we need to:
* Create a `Dockerfile` in which we define how the docker image 
must be build in order to run our application
```python
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["python", "app.py"]
```
* Build our docker image : `docker build -t my_dash_app .`
* Run a container : need to expose port `8050` which is the port used by plotly dash
with the command `docker run -p 8050:8050 my_dash_app`.

In order to make our application accessible from outside the container,
we need to set the host to `0.0.0.0`, we can do it by update the run server :
```python
app.run_server(host='0.0.0.0', port=8050, debug=True)
```

### Last part - Push the app in GitHub
As you see it in GitHub we need to create a repository to share the app
To do that we just need to follow the command lines after creating
the repository



