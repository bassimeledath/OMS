########import all libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import plotly.plotly as py
import plotly.graph_objs as go

import base64
import datetime
import io

from random import uniform

import numpy as np
import pandas as pd

#######load data
df = pd.read_csv('plot_data.csv')
df = df.iloc[:, ~df.columns.str.contains('^Unnamed')]

#######columns
size = df['size'].values
score = df['engagement_score'].values
click = df['click_score'].values
view = df['view_sum'].values
session = df['session_length'].values

#######css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#######colors
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'blueish': '#00A6C6',
    'goldish': '#FFDF00'
}

#######globals
x_axis = ['30-day', '60-day', '90-day']

#######important functions
def calcu(s, d):
    res = (s * d).sum()
    to_show = [res]
    for i in range(2):
        rand = uniform(0.6, 1)
        to_sub = res * rand
        to_show.append(to_sub)
    return to_show

#######instantiate app
app = dash.Dash("Wells-Carbo", external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.RadioItems(id='choice',
                options=[
                    {'label': 'Current', 'value': '1'},
                    {'label': 'Increase Offers Shown', 'value': '2'},
                ],
                value='1',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'marginLeft': '5%', 'marginTop': '5%'}),
        html.Div(id='more', children=[
            html.Div(id='hyp-prop', children=[
                html.H4('Cluster 1'),
                html.H6('Very Low Click Count', style={'marginLeft': '3%'}),
                html.H4('Cluster 2'),
                html.H6('High Click Through Rate', style={'marginLeft': '3%'}),
                html.H4('Cluster 3'),
                html.H6('High Login Rate', style={'marginLeft': '3%'}),
                dcc.Graph(id='engage-s')
            ], style={'height': '80%', 'width': '40%', 'marginLeft': '9%'}),
            dcc.Graph(id='engage-score')
        ], style={'columnCount': 2})
    ]),
    html.Div(id='less', children=[
        dcc.Graph(id='session-length'),
        dcc.Graph(id='view-count'),
        dcc.Graph(id='alert-count')
    ], style={'columnCount': 3})
])

#######create callbacks
@app.callback(
    Output('engage-score', 'figure'),
    [Input('choice', 'value')]
)
def score_plot(value):
    if value == '2':
        pass
    y_values = calcu(size, score)
    plot = go.Bar(
            x=x_axis,
            y=y_values,
            marker=dict(color='#00A6C6')
    )
    return {
        'data': [plot],
        'layout': go.Layout(
            hovermode='closest',
            yaxis= dict(title='BasSam Engagement Score')
        )
    }

@app.callback(
    Output('session-length', 'figure'),
    [Input('choice', 'value')]
)
def session_plot(value):
    if value == '2':
        pass
    y_values = calcu(size, session)
    plot = go.Bar(
            x=x_axis,
            y=y_values,
            marker=dict(color='#FFDF00')
    )
    return {
        'data': [plot],
        'layout': go.Layout(
            hovermode='closest',
            yaxis= dict(title='Session Length')
        )
    }

@app.callback(
    Output('view-count', 'figure'),
    [Input('choice', 'value')]
)
def view_count_plot(value):
    if value == '2':
        pass
    y_values = calcu(size, view)
    plot = go.Bar(
            x=x_axis,
            y=y_values,
            marker=dict(color='#B22222')
    )
    return {
        'data': [plot],
        'layout': go.Layout(
            hovermode='closest',
            yaxis= dict(title='Number of Views')
        )
    }

@app.callback(
    Output('alert-count', 'figure'),
    [Input('choice', 'value')]
)
def view_alert_count(value):
    if value == '2':
        pass
    y_values = calcu(size, click)
    plot = go.Bar(
            x=x_axis,
            y=y_values
    )
    return {
        'data': [plot],
        'layout': go.Layout(
            hovermode='closest',
            yaxis= dict(title='Number of Clicks')
        )
    }


#######run app
if __name__ == '__main__':
    app.run_server(debug=True)
