import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
import dash
import plotly.graph_objs as go
import base64
import pickle
from random import randint as rnum

DF_SAMPLE = pd.DataFrame({
        "Employee's Satisfaction level":[2],"Number of projects":[9],
        "Time with company":[18], "Promoted in last 5 years":["Yes"],
        "Department":"Sales", "Salary":["Medium"], "Average Monthly Hours":[310],
        "Work Accident":['No'],"Last Evaluation":[0.85]
})

app = dash.Dash()
server = app.server

app.title = 'HR Analytics'

# app layout
layout = html.Div([
                # Create app title
                html.Div([html.Div([html.H3('Employee Attrition prediction', style={'textAlign':'center', 'color':'white'})],
                className="gs-text-header"),

                #html.Div([], className='four columns'),
                html.Div([html.H6('Enter the parameters and click submit')],
                    style={'textAlign':'center', 'color':'steelblue'}),

                html.Br([]),
                html.Br([]),

                # Create dropdowns with parameters which will be inputed into model to return probability predicted
                html.P([
                    html.Label("Employee's Satisfaction level"),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='sat',
                        options=[{'label': i, 'value':i} for i in range(1,11)],
                        value=1
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Number of projects'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='proj',
                        options=[{'label': i, 'value':i} for i in range(0,45)],
                        value=0
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Time with company'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='comp',
                        options=[{'label': i, 'value':i} for i in range(1,48)],
                        value=1
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Promoted in last 5 years'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='prom',
                        options=[{'label': 'Yes', 'value':1}, {'label':'No', 'value':0}],
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),


                html.P([
                    html.Label('Department'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='dept',
                        options=[{'label': 'Sales', 'value':'sales'},           {'label':'Accounting', 'value':'accounting'},
                                {'label': 'IT', 'value':'IT'},
                                {'label':'R&D', 'value':'RandD'},
                                {'label': 'HR', 'value':'hr'},
                                {'label':'Management', 'value':'management'},
                                {'label': 'Marketing', 'value':'marketing'},
                                {'label':'Product Management', 'value':'product_mng'},
                                {'label': 'Support', 'value':'support'},
                                {'label':'Technical', 'value':'technical'}
                        ],
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Salary'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='sal',
                        options=[{'label': 'Low', 'value':'low'}, {'label':'Medium', 'value':'medium'}, {'label':'High', 'value':'high'}],
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Work Accident'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Dropdown(
                        id='acci',
                        options=[{'label': 'Yes', 'value':1}, {'label':'No', 'value':0}],
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),

                html.P([
                    html.Label('Average Monthly Hours'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Input(
                        id='hours',
                        placeholder='Enter Average hours',
                        type='int',
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px',
                            'text-align': 'center',
                            'display':'inline-block', 'paddingTop':'10px'}),

                html.P([
                    html.Label('Last evalution'),
                    # dcc.Input(id='mother_birth', value=1952, type='number'),
                    dcc.Input(
                        id='eval',
                        placeholder='0.75 (Enter decimal %)',
                        type='int',
                        value=''
                    )
                    ],
                    style={'width': '200px', 'margin-right': '10px',
                            'margin-left': '10px', 'text-align': 'center',
                            'display':'inline-block'}),


                # html.Div([html.H5("Attrition Probability:")],
                #     style={'paddingLeft':'20px','width':'35%',
                #     'paddingTop':'10px','display':'inline-block'}),

                html.Div([
                    html.H4(id='pred', style={'paddingTop':'0px', 'paddingLeft':'10px','text-align':'left'})
                    ], style={'width':'65%', 'display':'inline-block',
                              'paddingRight':'70px'}),

                html.Div([
                html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize':28}
                )],style={ 'align':'right', 'width':'150px', 'display':'inline-block'}),

                html.Div([
                    html.Div([html.H6('Sample Employee details')],className= "gs-text-header", style={'color':'white'}),
                    dt.DataTable(
                        rows=DF_SAMPLE.to_dict('records'),

                        # optional - sets the order of columns
                        columns=sorted(DF_SAMPLE.columns),

                        editable=False,

                        id='editable-table'
                )]),

                # dcc.Textarea(
                #     placeholder='Result....',
                #     value='',
                #     style={'width': '15%', 'height': '2%', 'display':'inline-block'}
                # ),

                # Create Output box/plot to display the predicted probability
                html.Div([
                    dcc.Graph(id='pred_plot',
                              figure = {
                                'data': [
                                    go.Bar(
                                        y = ['Attrition Risk', 'Attrition Safe'],
                                        x = [62, 38],
                                        marker = dict(color = ['red','green']),
                                        orientation = 'h',
                                    )
                                ],
                               'layout':{'title':'Sample - Attrition Probability: 62%', 'hovermode':'closest', 'width':540, 'height':275}
                              }, config={'displayModeBar': False})
                ], className='container', style={'width':'70%','paddingLeft':'5px'}),

                # Create a section to display the visualizations created during EDA
                    #Create first visualizations wth callback options

                    # Create second visualiation exploring different aspect of the data analysis
                html.Div([html.H6("Live prediction not possible to different environment than on which model was trained. Use code from Github to generate the model and run Dash server to check the functioning, the above response is generated using random numbers as a proxy of what will happen on receiving predictions from the model. Anyway enter all the parameters and click submit to check the interactivity if you didn't do it.")], style={'textAlign':'center'}),
                html.Br([]),
                html.Br([]),

                # Information and link to access the dataset from kaggle code from github
                html.Div([dcc.Markdown('''Find out more about the data [Kaggle](https://www.kaggle.com/colara/hr-analytics). Get the code on [GitHub](https://github.com/PhotonSphere/HR_Analytics_app)''')], style={'textAlign':'center','color':'royalblue'})

    ], className="subpage"),
], className="page")

# assinging the layout to the app
app.layout = layout

# create Input and Output callbacks for the prediction part
@app.callback(
    #Output('pred', 'children'),
    Output('pred_plot', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('sat', 'value'),
    State('proj', 'value'),
    State('comp', 'value'),
    State('prom', 'value'),
    State('dept', 'value'),
    State('sal', 'value'),
    State('hours', 'value'),
    State('acci', 'value'),
    State('eval', 'value'),])
def output(n_clicks, sat, proj, comp, prom, dept, sal, hours, acci, eval):

    if sat != '' and proj != '' and comp != '' and  prom!= '' and dept != '' and sal != '' and hours != '' and acci != '' and eval != '':

        try:
            ## generating ValueError for testing to run code in exception
            ### errgen = int('a')
            objects = []
            with open('final_model.pkl', 'rb') as f:
                objects.append(pickle.load(f))


            if float(eval) < 0.6:
                underperformer = 1
            else:
                underperformer = 0

            if float(sat)/10 < 0.2:
                unhappy = 1
            else:
                unhappy = 0

            if float(eval) > 0.8 and float(sat)/10 > 0.7:
                overachiever = 1
            else:
                overachiever = 0

            if sal == 'high':
                salary_high = 1
                salary_medium = 0
                salary_low = 0
            elif sal == 'medium':
                salary_high = 0
                salary_medium = 1
                salary_low = 0
            elif sal == 'low':
                salary_high = 0
                salary_medium = 0
                salary_low = 1

            if dept == 'sales':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 1
                Department_support = 0
                Department_technical = 0
            elif dept == 'accounting':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 1
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'IT':
                Department_IT = 1
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'RandD':
                Department_IT = 0
                Department_RandD = 1
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'hr':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 1
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'management':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 1
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'marketing':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 1
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'product_mng':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 1
                Department_sales = 0
                Department_support = 0
                Department_technical = 0
            elif dept == 'support':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 1
                Department_technical = 0
            elif dept == 'technical':
                Department_IT = 0
                Department_RandD = 0
                Department_accounting = 0
                Department_hr = 0
                Department_management = 0
                Department_marketing = 0
                Department_product_mng = 0
                Department_sales = 0
                Department_support = 0
                Department_technical = 1

            data = pd.DataFrame(
                    {'satisfaction_level':[sat/10], 'last_evaluation':[eval],
                     'number_project':[proj], 'average_monthly_hours':[hours],
                     'time_spend_company':[comp], 'Work_accident':[acci],
                     'promotion_last_5years':[prom], 'underperformer':[underperformer], 'unhappy':[unhappy],
                     'overachiever':[overachiever], 'Department_IT':[Department_IT], 'Department_RandD':[Department_RandD],
                     'Department_accounting':[Department_accounting], 'Department_hr':[Department_hr], 'Department_management':[Department_management], 'Department_marketing':[Department_marketing],
           'Department_product_mng':[Department_product_mng], 'Department_sales':[Department_sales], 'Department_support':[Department_support],
           'Department_technical':[Department_technical], 'salary_high':[salary_high], 'salary_low':[salary_low], 'salary_medium':[salary_medium]}
            )

            #return dt.DataTable(rows=data.to_dict('records'))
            pred = objects[0].predict_proba(data)
            attrition_risk = [p[1] for p in pred][0] * 100
            attrition_safe = [p[0] for p in pred][0] * 100
            #return attrition_risk

            figure = go.Figure(
                    data = [
                        go.Bar(
                            y = ['Attrition Risk'],
                            x = [attrition_risk],
                            marker = dict(color='red'),
                            name = 'Risk',
                            orientation = 'h'
                        ),

                        go.Bar(
                            y = ['Attrition Safe'],
                            x = [attrition_safe],
                            marker = dict(color='green'),
                            name = 'Safe',
                            orientation = 'h'
                        )
                    ],

                    layout = dict(
                            title = "Attrition Probability {}%".format(int(attrition_risk)),
                            yaxis = dict(
                                        showgrid=False,
                                        showline=False,
                                        showticklabels=True,
                                        domain = [0,1]
                            ),
                            hovermode = 'closest',
                            width = 540, height = 275
                    )
            )
        except ValueError:
            ran_att = rnum(1, 100)
            figure = {
              'data': [
                  go.Bar(
                      y = ['Attrition Risk', 'Attrition Safe'],
                      x = [ran_att, 100-ran_att],
                      marker = dict(color = ['red','green']),
                      orientation = 'h',
                  )
              ],
             'layout':{'title':"Attrition Probability " + (str(ran_att) + '%'), 'hovermode':'closest', 'width':540, 'height':275
                    }
            }



        return figure
# create Input and Output callback functions for the EDA part


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

# call to run the server
if __name__ == '__main__':
    app.run_server()
