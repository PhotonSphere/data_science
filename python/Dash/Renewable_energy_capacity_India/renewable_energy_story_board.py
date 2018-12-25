import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import base64

df = pd.read_csv('RE_Dash_data.csv')

app = dash.Dash()
server = app.server

app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75'
        '/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'
    )
})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def encode_image(image_file):
    """
        Function to read the image file and render
        the html format for embedding static images
    """
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

# contains the layout for entire dashboard
layout = html.Div([

    html.Br([]),

    dcc.Markdown('''
    ### WHY 24 CR INDIANS WITHOUT POWER ARE COUNTING ON SUN, WIND

    ***
    '''.replace('  ',''), className='container',
    containerProps={'style':{'maxwidth':'300px','textAlign':'center'}},
    ),

    html.Div(
        dcc.Markdown('''
            ##### As India's renewable costs tumble, sector to see $175bn investment
        '''.replace('  ',''), className='container'
        ), style={
            'textAlign': 'center',
            'color': colors['text'],
            'width': '40%', 'display': 'inline-block',
            'paddingLeft':120}),

    html.Div(
        dcc.Markdown('''
            ##### Coal-based power plants still produce 60% of India's power
        '''.replace('  ',''), className='container'
        ), style={
            'textAlign': 'center',
            'color': colors['text'],
            'width': '40%', 'display': 'inline-block',
            'paddingLeft':20}),

    html.Div(
        dcc.Markdown('''
            ##### By 2035 India's energy consumption is expected to grow the fatest among the major enconomies and renewables are set to play a big part - in particular for the 24 core Indians still without electricity
        '''.replace('  ',''), className='container'
        ), style={
            'textAlign': 'right',
            'color': colors['text'],
            'width': '40%', 'display': 'inline-block',
            'paddingLeft':120, 'paddingTop':0}),

    html.Div([
    dcc.Interval(id='interval-component',
                 interval=600000000,
                 n_intervals=0),
    html.Img(id='hover-image', src='children', height=250)
    ], style={'paddingLeft':50, 'width': '30%', 'display': 'inline-block',
              'contentAlign':'right'}),

    html.Br([]),

    dcc.Markdown('''
    ***
    ##### India is energy hungry, dependent mostly on coal, but renewables are on the rise
    '''.replace('  ',''), className='container',
    containerProps={'style':{'maxwidth':'300px','textAlign':'center'}},
    ),


        html.Div([dcc.Markdown('''
                        ##### No.3
                        India is behind only China
                        and US in energy use'''.replace('  ',''), className='container',
                        containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'paddingLeft':180, 'width': '20%'}),

        html.Div([dcc.Markdown('''
                        ##### 67%
                        Electricity from fossil fuels, mostly coal
                        '''.replace('  ',''), className='container',
                        containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'width':'20%', 'paddingLeft':50} ),

        html.Div([dcc.Markdown('''
                        ##### 20%
                        Energy from renewable sources; thermal generation capacity stagnant; was at 59% in 2003 and 2017
                        '''.replace('  ',''), className='container',
                        containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'width':'35%', 'paddingLeft':10}),

    html.Div([dcc.Markdown('''
                    ##### 2X
                    Energy use has doubled since 2000, but consumption per capita is around one-third of global average
                    ##### 11%
                    Of global coal consumption in India, making it world's second-largest coal consumer. Reliance on coal will continue'''.replace('  ',''), className='container',
                    containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'paddingLeft':180, 'width': '20%'}),

    html.Div([dcc.Markdown('''
                    ##### 35%
                    What coal-based power contributes to the total all-India CO2 emissions

                    ##### 40%
                    Installed capacity by 2030 from non-fossil-fuel-based resources - mostly renewable energy
                    '''.replace('  ',''), className='container',
                    containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'width':'20%', 'paddingLeft':50} ),

    html.Div([
            dcc.Graph(id='pie1',
                figure = {
                    'data': [ {
                        'values': [20, 80],
                        'marker': {'colors': ['rgb(34,139,34)',
                                            'rgb(241, 236, 225)'
                                  ]},
                        'type': 'pie',
                        'text':['Renewable Energy','Thermal'],
                        'mode':'none',
                        'hoverinfo':'none',
                        'textinfo':'none'
                        }],
                    'layout': {'showlegend': False, 'height':150, 'autosize': True, 'margin' : {
                                  "r": 0,
                                  "t": 0,
                                  "b": 10,
                                  "l": 10},
                                  'annotations':[
                dict(
                    text="20% Renewables' share",
                    showarrow=False,
                    arrowhead=7,
                    ax=10,
                    ay=-50
                )
            ]}
                }, config={
'displayModeBar': False})], style={'display':'inline-block', 'width':'20%', 'height':'5%', 'paddingLeft':10, 'paddingTop':0}),

    html.Br([]),

    html.Div([dcc.Markdown('''***''', className='container',
    containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

    html.Div([
        dcc.Graph(id='capacitymix',
            figure={'data': [go.Bar(
                x=df['Year'],
                y=df['Coal'],
                text='Coal',
                name='',
                marker=dict(
                    color='rgb(169,169,169)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            ),
            go.Bar(
                x=df['Year'],
                y=df['Gas'],
                text='Gas',
                name='',
                marker=dict(
                    color='rgb(211,211,211)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            ),
            go.Bar(
                x=df['Year'],
                y=df['Diesel'],
                text='Diesel',
                name='',
                marker=dict(
                    color='rgb(191, 57, 34)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            ),
            go.Bar(
                x=df['Year'],
                y=df['Nuclear'],
                text='Nuclear',
                name='',
                marker=dict(
                    color='rgb(221, 175, 39)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            ),
            go.Bar(
                x=df['Year'],
                y=df['Hydro'],
                text='Hydro',
                name='',
                marker=dict(
                    color='rgb(24, 130, 201)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            ),
            go.Bar(
                x=df['Year'],
                y=df['Renewable Energy'],
                text='Renewable Energy',
                name='',
                marker=dict(
                    color='rgb(34,139,34)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=0,
                    )
                )
            )
            ],
            'layout':go.Layout(barmode='stack', hovermode='closest', title="Renewables' share in India's installed capacity has been steadily growing", xaxis=dict(tickangle=-45),
            showlegend= False, autosize= True, margin = {
                          "r": 0,
                          "t": 25,
                          "b": 35,
                          "l": 20},
                          annotations=[
                      dict(
                          x=2008,
                          y=1.1,
                          xref='x',
                          yref='y',
                          text='Installed capacity mix',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=0
                      ),
                      dict(
                          x=2007,
                          y=0.97,
                          xref='x',
                          yref='y',
                          text='6%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2007,
                          y=0.8,
                          xref='x',
                          yref='y',
                          text='26%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2007,
                          y=0.58,
                          xref='x',
                          yref='y',
                          text='10%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2007,
                          y=0.39,
                          xref='x',
                          yref='y',
                          text='54%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2009,
                          y=0.8,
                          xref='x',
                          yref='y',
                          text='Hydro',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2009,
                          y=0.57,
                          xref='x',
                          yref='y',
                          text='Gas',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2009,
                          y=0.3,
                          xref='x',
                          yref='y',
                          text='Coal',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2018,
                          y=0.95,
                          xref='x',
                          yref='y',
                          text='20%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2018,
                          y=0.7,
                          xref='x',
                          yref='y',
                          text='13%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2018,
                          y=0.6,
                          xref='x',
                          yref='y',
                          text='7%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2018,
                          y=0.5,
                          xref='x',
                          yref='y',
                          text='57%',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      ),
                      dict(
                          x=2014,
                          y=0.95,
                          xref='x',
                          yref='y',
                          text='Renewable Energy',
                          showarrow=False,
                          arrowhead=7,
                          ax=0,
                          ay=-10
                      )
                  ])}, config={'displayModeBar': False}
        )
    ], style={'display':'inline-block', 'width':'48%', 'height':'60%', 'paddingLeft':140, 'paddingTop':10}),


    html.Div([
        dcc.Graph(id='pie2',
        figure = {
            'data': [ {
                'values': [80, 20],
                'marker': {'colors': ['rgb(34,139,34)',
                                    'rgb(241, 236, 225)'
                          ]},
                'type': 'pie',
                #'text':['Renewable Energy','Thermal'],
                'textinfo':'none',
                'mode':'none',
                'hoverinfo': 'none'
                }],
            'layout': {'showlegend': False, 'height':120, 'autosize': True, 'margin' : {
                          "r": 0,
                          "t": 15,
                          "b": 10,
                          "l": 10},
                          'annotations':[
            dict(
                text='80% decline',
                showarrow=False,
                arrowhead=7,
                ax=10,
                ay=-50
            )
                ]}
                    }, config={
            'displayModeBar': False}),

dcc.Markdown('''
                ##### Clean Power now cheaper
                **80%** decline in tariffs for solar energy since 2010, owing to factors like **drop in** photovoltaic module **cost**, increase in scale of projects, etc.
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'width':'15%', 'height':'55%', 'paddingLeft':5, 'paddingTop':0}
    ),

    html.Div([
    dcc.Graph(id='pie3',
        figure = {
            'data': [ {
                'values': [50, 50],
                'marker': {'colors': ['rgb(34,139,34)',
                                    'rgb(241, 236, 225)'
                          ]},
                'type': 'pie',
                #'text':['Renewable Energy','Thermal'],
                'textinfo':'none',
                'mode':'none',
                'hoverinfo':'none'
                }],
            'layout': {'showlegend': False, 'height':120, 'autosize': True, 'margin' : {
                          "r": 0,
                          "t": 10,
                          "b": 10,
                          "l": 10},
                          'annotations':[
                dict(
                    text='50% decline',
                    showarrow=False,
                    arrowhead=7,
                    ax=10,
                    ay=-50
                )
            ]}
                }, config={
        'displayModeBar': False}),

dcc.Markdown('''
                **50%** drop in wind energy tariff in less than a year, thanks to competitive bidding in wind sector introduced in 2017.
                Both **wind and solar energy tariffs**
                are now less than the conventional sources
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'100px','textAlign':'left'}})], style={'display':'inline-block', 'width':'15%', 'height':'65%', 'paddingLeft':5, 'paddingTop':0}
    ),

    html.Br([]),

    html.Div([
        dcc.Markdown('''
            ***
            #### Renewable energy could become as affordable as conventional sources
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

    html.Div([
        dcc.Graph(
            id='tarriff',
            figure={'data': [
                        go.Bar(
                            x=df['Financial Year'],
                            y=df['Thermal'],
                            text='Thermal Tariff',
                            name='',
                            #text='Thermal',
                            #orientation='h',
                            marker=dict(
                                color='rgb(152,251,152)',
                                line=dict(
                                    color='rgb(8,48,107)',
                                    width=0,
                                )
                            )
                        ),
                        go.Bar(
                            x=df['Financial Year'],
                            y=df['Wind'],
                            text='Wind Tariff',
                            name='',
                            #text='Wind',
                            #orientation='h',
                            marker=dict(
                                color='rgb(50,205,50)',
                                line=dict(
                                    color='rgb(8,48,107)',
                                    width=0,
                                )
                            )
                        ),
                        go.Bar(
                            x=df['Financial Year'],
                            y=df['Solar'],
                            text='Solar Tariff',
                            name='',
                            #text='Solar',
                            #orientation='h',
                            marker=dict(
                                color='rgb(34,139,34)',
                                line=dict(
                                    color='rgb(8,48,107)',
                                    width=0,
                                )
                            )
                        )
                        ],
                    'layout': go.Layout(
                            barmode='group',
                            showlegend= False, autosize=True,margin= {
                                  "r": 0,
                                  "t": 10,
                                  "b": 20,
                                  "l": 10},
                                  xaxis=dict(
                                      showgrid=False,
                                      #showline=False,
                                      #showticklabels=False,
                                      zeroline=False,
                                      domain=[0.15, 1],
                                      #side='top'
                                  ),
                                  yaxis=dict(
                                        showgrid=False,
                                        #showline=False,
                                        #showticklabels=False,
                                        zeroline=False,
                                    ),
                                hovermode='closest',
                                annotations=[
                                    dict(
                                        x=2014,
                                        y=8.49,
                                        text='Rs/kWh',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2013.72,
                                        y=5.1,
                                        text='4.9',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2013.97,
                                        y=5.15,
                                        text='5',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2014.25,
                                        y=8.09,
                                        text='7.9',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2015.3,
                                        y=6.75,
                                        text='6.5',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2016,
                                        y=7.8,
                                        text='Decline in solar tariff from Rs 15/kWh in 2010',
                                        showarrow=False,
                                        ax=0,
                                        ay=0,
                                        font=dict(
                                            family='Courier New, monospace',
                                            #size=16,
                                            color='rgb(34,139,34)'
                                            ),
                                        opacity=0.8
                                    ),
                                    dict(
                                        x=2018.25,
                                        y=2.6,
                                        text='2.4',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2017.98,
                                        y=2.6,
                                        text='2.4',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2017.72,
                                        y=5.1,
                                        text='4.9',
                                        showarrow=False,
                                        ax=0,
                                        ay=0
                                    ),
                                    dict(
                                        x=2017,
                                        y=5.5,
                                        text='Solar & Wind tariff achieve grid parity in 2018',
                                        showarrow=False,
                                        ax=0,
                                        ay=0,
                                        font=dict(
                                            family='Courier New, monospace',
                                            #size=16,
                                            color='rgb(34,139,34)'
                                            ),
                                        opacity=0.8
                                    )
                                ]
                        )
                    },config={'displayModeBar': False}
        )
    ], style={'display':'inline-block', 'width':'48%', 'height':'60%', 'paddingLeft':70, 'paddingTop':10}),

    html.Div([
        dcc.Markdown('''
                #### 275 GW
                ##### Targeted renewable energy capacity by 2027. India's total installed capacity was 61 GW in 2017
                ***
                #### $175bn
                ##### Investment that may flow into renewables over 10 years; solar & wind to account for more than 90%
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'left'}})
    ], style={'display':'inline-block', 'width':'35%', 'height':'60%', 'paddingLeft':15, 'paddingTop':10}),

    html.Br([]),

    html.Div([
        dcc.Markdown('''
            ***
            #### Why there is increase in renewables' share in capacity mix?
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

    html.Div([
        dcc.Markdown('''
            ### Paris green pact pushing clean break
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'left'}}),
    ], style={'display':'inline-block', 'width':'20%', 'height':'8%', 'paddingLeft':150, 'paddingTop':10}),

    html.Div([
        dcc.Markdown('''
            #### 33% - 35%
            ##### India's pledge to reduce emissions intensity of its GDP by 2030 from the 2005 level as part of its Nationally Determined Contributions under Paris climate pact
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'left'}}),
    ], style={'display':'inline-block', 'width':'50%', 'height':'10%', 'paddingLeft':45, 'paddingTop':10}),

    html.Div([
        dcc.Markdown('''
            ***
        '''.replace('  ',''), className='container',
        containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

        html.Div([
            dcc.Markdown('''
                Source: The Evolving Energy Landscape in India Study By Deloitte,
                This Story Board is a adaptation of the article published in Times of India on May 19, 2018
            ''')
            ], style={'paddingLeft':90}),

        html.Div([
            dcc.Markdown('''Find out more about the data, get the code on [GitHub](https://github.com/PhotonSphere/renewable_energy_app)''')], style={'paddingLeft':170})

])

# assinging the layout variable to app.layout
app.layout = layout

#calling callback to render the bulb image in first page
@app.callback(
    Output('hover-image', 'src'),
    [Input('interval-component', 'n_intervals')])
def callback_image(hoverData):
    path = 'RE2.jpg'
    return encode_image(path)

# running the app
if __name__ == '__main__':
    app.run_server()
