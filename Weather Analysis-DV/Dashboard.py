import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

df = pd.read_csv('weather1.csv')
df1 = df.iloc[np.r_[0:40, -40:0]]
countries=df["Station_State"].unique()
df2 = pd.read_csv('Mean_Temp.csv')
df2 = df2.set_index('YEAR')
time_durations = df2.columns

app = dash.Dash(__name__)

app.layout = html.Div(style={'background-image': 'url(https://image.freepik.com/free-vector/white-abstract-background_23-2148810113.jpg'},children=[
    html.Hr(),
    html.Div([html.H1(children='WEATHER ANALYSIS DASHBOARD',style={'textAlign': 'center','fontSize':40,'color': 'red'})]),
    html.Hr(),
    html.Div([
        html.Div([
            html.H1(children='PIE CHART',style={'textAlign': 'center','fontSize':35}),
                html.P("Names:",style={'fontSize':23}),

    dcc.RadioItems(
    id='names',
    options=[{'value': x, 'label': x} 
                 for x in ['Date_Year', 'Station_State']],
    value='Date_Year',
    labelStyle={'display': 'inline-block'}
),
    html.P("Values:",style={'fontSize':23}),
    dcc.RadioItems(
        id='values', 
        options=[{'value': x, 'label': x} 
                 for x in ['Data_Temperature_Avg_Temp', 'Data_Wind_Speed']],
        value='Data_Temperature_Avg_Temp',
    ),
    dcc.Graph(id="pie-chart"),],className ='six columns'),
    html.Hr(),
    html.Hr(),
    html.Br(),
    html.Div([
    html.H1(children='SCATTER PLOT--WIND SPEED Vs AVERAGE TEMPERATURE',style={'textAlign': 'center','fontSize':35}),
    dcc.Graph(id="scatter-plot"),

   
    html.P("Average Temperature:",style={'fontSize':25}),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=100, step=1,
        marks={10: '10', 100: '100'},
        value=[20, 30]
    ),
    ], className='six columns'),
    ], className='row'),
    html.Br(),
    html.Hr(),

    html.Div([
        html.Hr(),
         html.H1(children='BAR CHART--DATE Vs AVERAGE TEMPERATURE',style={'textAlign': 'center','fontSize':35}),
   dcc.Dropdown(
        id="dropdown", 
        options=[{"label": x, "value": x} for x in countries],
        value=countries[0], 
        clearable=False
    ),
     dcc.Graph(id="bar-chart"),
      ], className='row'),

    html.Div([
        html.Hr(),
         html.Hr(),
        html.Br(),
            html.H1(children='AVERAGE TEMPERATURE ANALYSIS',style={'textAlign': 'center','fontSize':35}),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='time_durs',
                options=[{'label': i, 'value': i}
                         for i in time_durations],
                value='ANNUAL',
                placeholder='Select Month/time duration'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic'),
   ], className='row'),   
])


@app.callback(
    Output("pie-chart", "figure"), 
    [Input("names", "value"), 
     Input("values", "value")])
def generate_chart(names, values):
    fig = px.pie(df1, values=values, names=names)
    return fig

@app.callback(
    Output("scatter-plot", "figure"), 
    [Input("range-slider", "value")])
def update_scatter_plot(slider_range):
    low, high = slider_range
    mask = (df['Data_Temperature_Min_Temp'] > low) & (df['Data_Temperature_Max_Temp'] < high)
    fig = px.scatter(
        df[mask], x="Data_Wind_Speed", y="Data_Temperature_Avg_Temp", 
        color="Station_State", size='Data_Wind_Direction')
    return fig

@app.callback(
   Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(Station_State):
    mask = df["Station_State"] == Station_State
    fig = px.bar(df[mask], x="Date_Full", y="Data_Temperature_Avg_Temp",color="Date_Month",barmode="group")
    return fig

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('time_durs', 'value')])
def update_graph(month):
    dff = df2[month]
    dff_roll = dff.rolling(20, min_periods=5).mean()

    return {
        'data': [go.Scatter(
            x=list(dff.index),
            y=dff.values,
            name='Temprature',
            mode='lines+markers'
        ), go.Scatter(
            x=list(dff_roll.index),
            y=dff_roll.values,
            name='Rolling Mean',
            mode='lines+markers'
        )],
        
        'layout': {
            'height': 525,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)'
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }   

app.run_server(debug=True)