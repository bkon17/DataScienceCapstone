
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 19:02:19 2023

@author: Ben Kon
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label':'All Sites', 'value':'ALL'},
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder="All Sites",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                2000: '2000',
                                                4000: '4000',
                                                6000: '6000',
                                                8000: '8000',
                                                10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum()
        fig = px.pie(spacex_df, values=filtered_df.values, 
        names=filtered_df.index, 
        title='Successes of All Launch Sites')
        fig.update_layout()
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class')['class'].count()
        fig = px.pie(filtered_df, names=['Failure', 'Success'], values=filtered_df.values, title='Success Rate of {} Launch Site'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                    Input(component_id='site-dropdown', component_property='value'),
                    Input(component_id='payload-slider', component_property='value'))
def get_scatter(site_entry, payload_entry):
    pl_range = payload_entry
    dff=spacex_df[spacex_df['Payload Mass (kg)'].between(pl_range[0],pl_range[1])]
    if site_entry == 'ALL':
        fig = px.scatter(dff, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success vs Failure for Selected Payload Mass Range at All Launch Sites', labels={'class':'Success vs Failure'})
        return fig
    else:
        dfinal = dff[dff['Launch Site'] == site_entry]
        fig = px.scatter(dfinal, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success vs Failure for Selected Payload Mass Range at {} Launch Site'.format(site_entry), labels={'class':'Success vs Failure'})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)
