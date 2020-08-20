import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input 

from sqlalchemy import create_engine

app = dash.Dash(__name__)

engine = create_engine('postgresql://odoo@localhost:5443/test_dw')

psql_qery = """
select
so.latitude as lat
,so.longitude  as lon
,so.province as province
,sum(oi.qty) as total_qty
from order_item as oi
left join sale_order as so on oi.order_id = so.id
group by
so.latitude
,so.longitude
,so.province
"""

df = pd.read_sql_query(psql_qery, con=engine)
df.reset_index(inplace=True)

app.layout = html.Div([
    html.H1('TEST Python Dashboard', style={'text-align': 'center'}),
    dcc.Dropdown(
        id='select_year',
        options=[
            {'label': '2015', 'value': 2015},
            {'label': '2016', 'value': 2016},
            {'label': '2017', 'value': 2017},
            {'label': '2018', 'value': 2018},
        ],
        multi=False,
        value=2015,
        style={'width': '40%'}
        ),

    # html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])

@app.callback(
    # [Output(component_id='output_container', component_property='children'), 
     Output(component_id='my_bee_map', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(values):
    df_cp = df.copy()
    container = "The year chosen by user was: {}".format(values)
    df_cp['lat'] = df['lat'].astype('float64')
    df_cp['lon'] = df['lon'].astype('float64')
    px.set_mapbox_access_token('pk.eyJ1IjoiYXVrcml0NTU1IiwiYSI6ImNrZTE3aXF6cDA4czQycXA0OGZ1d2d1ZWIifQ.2FANyPUkQZ7J10tk3kZSog')
    fig = px.scatter_mapbox(df_cp, lat="lat", lon="lon", text='province',
                            color="total_qty", size="total_qty",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)
    
    # fig = go.Figure(go.Scattermapbox(
    #     lat=df_cp['lat'],
    #     lon=df_cp['lon'],
    #     mode='markers',
    #     marker=go.scattermapbox.Marker(
    #         size=14
    #     ),
    #     text=df_cp['province'],
    # ))

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiYXVrcml0NTU1IiwiYSI6ImNrZTE3aXF6cDA4czQycXA0OGZ1d2d1ZWIifQ.2FANyPUkQZ7J10tk3kZSog',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=13,
                lon=100
            ),
            pitch=0,
            zoom=5
        ),
        height=800
    )
    
    return fig
    
    
# run main function
if __name__ == '__main__':
    app.run_server(debug=True)