import pandas as pd
import numpy as np
##from flask import Flask, session
##from flask_session import Session
import dash_html_components as html
import dash_core_components as dcc
import dash
import plotly.graph_objs as go
import base64
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
from time import sleep

css = [
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/30b641e2e89753b13e6557b9d65649f13ea7c64c/dash-docs-custom.css',
    'https://fonts.googleapis.com/css?family=Dosis',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css'
]

# function which generates the html table for BMI and HWR classification
def generate_table(dataframe, max_rows=10, highlight=0):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

questions = pd.read_csv("question_quotes.csv")

# creating variables for data, question and quotes dict
data = questions
d_dict = {}
m_dict = {}

# the correct answers list variable to provide feedback
#expected_answer = ['First insight: Never skip your Breakfast. "Now check the correct answer and click SUBMIT, then NEXT for more questions"']
expected_answer = 'First insight: Never skip your Breakfast. "Now check the correct answer and click SUBMIT, then NEXT for more questions"'

click1_count = 0
click2_count = 0

# making a dict for questions and quotes
for i in range(len(data)):
	#d_dict[i]= data.iloc[i]
	m_dict[i]= data.iloc[i]['Motivation']

question_df = data[['Question','Answer','W1','W2']].dropna()
for i in range(len(question_df)):
	d_dict[i] = question_df.iloc[i]

# randomizing the question order
#num_of_ques = int(data.iloc[0]['NQ'])
num_of_ques = len(data['Question'].dropna())
question_nums = list(range(num_of_ques))
question_order = np.random.choice(question_nums, num_of_ques, replace=False)
question_index = 0

questions_count = []
mot_count = []

COLORS = [
    {
        'background': '#fef0d9',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fdcc8a',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fc8d59',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#d7301f',
        'text': 'rgb(30, 30, 30)'
    },
]

# function to check the type of inputs for BMI and HWR section
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# function to style the feedback for
def cell_style(value, min_value, max_value):
    style = {}
    if is_numeric(value):
        relative_value = (value - min_value) / (max_value - min_value)
        if relative_value <= 0.25:
            style = {
                'backgroundColor': COLORS[0]['background'],
                'color': COLORS[0]['text']
            }
        elif relative_value <= 0.5:
            style = {
                'backgroundColor': COLORS[1]['background'],
                'color': COLORS[1]['text']
            }
        elif relative_value <= 0.75:
            style = {
                'backgroundColor': COLORS[2]['background'],
                'color': COLORS[2]['text']
            }
        elif relative_value <= 1:
            style = {
                'backgroundColor': COLORS[3]['background'],
                'color': COLORS[3]['text']
            }
    return style


def generate_table_result(dataframe, max_rows=100):
    max_value = df.max(numeric_only=True).max()
    min_value = df.min(numeric_only=True).max()
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            style = cell_style(value, min_value, max_value)
            row.append(html.Td(value, style=style))
        rows.append(html.Tr(row))

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        rows)

BMI_df = pd.DataFrame({'BMI (kg/m^2)':['less than 18.5','18.5 - 24.9','25 - 29.9','30 - 34.9','35 - 39.9','40 upwards'],
                      'Classification':['underweight','normalweight','overweight','class I obese','class II obese','class III obese']})

WTH_df = pd.DataFrame({'Female':['0.80 or lower','0.81 to 0.84','0.85 or higher'],
                       'Male':['0.95 or lower','0.96 to 1.0','1.0 or higher'],
                       'Health Risk':['Low risk','Moderate risk','High risk']})

# header = html.Div(
#     className='header',
#     children=html.Div(
#         className='container-width',
#         style={'height': '100%'},
#         children=[
#             # html.A(html.Img(
#             #     src='https://cdn.rawgit.com/plotly/dash-docs/b1178b4e/images/dash-logo-stripe.svg',
#             #     className='logo'
#             # ), href='https://plot.ly/products/dash', className='logo-link'),
#
#             html.Div(className='links', children=[
#                 html.A('pricing', className='link', href='https://plot.ly/dash/pricing'),
#                 html.A('workshops', className='link', href='https://plotcon.plot.ly/'),
#                 html.A('user guide', className='link active', href='/'),
#                 html.A('plotly', className='link', href='https://plot.ly/'),
#                 html.A(children=[html.I(className="fa fa-search")], className='link', href='/search')
#             ])
#         ]
#     )
# )



app = dash.Dash()
server = app.server

app.title = 'AIM Fitness'

layout = html.Div([

            #header,

            # create visual title

            html.Div([html.H3('Awareness --> Insights --> Motivation'),
                     html.H5('AIM for good health')],
                     className='content-container container-width', style={'textAlign':'center', 'backgroundColor':'#9999FF'}),

            #html.Div(style={'width':'25%','display':'inline-block'}),

            html.Div([html.H3('Awareness of health level')],
                    #className='content-container container-width',
                    style={'textAlign':'center', 'backgroundColor':'#76D7C4','width':'30%',
                            #'marginLeft':'460px',
                            'margin':'auto'}),

            #html.Div([],style={'width':'5%','display':'inline-block'}),

            # create div to caputre inputs for BMI calculation, aligned left
            html.Div([
                    html.H4('BMI Calculator'),
                    html.P([
                        html.Label('Weight (Kgs)'),
                        dcc.Input(
                                id='weight',
                                type='float',
                                placeholder='Enter weight in Kgs',
                        )]),

                    html.P([
                        html.Label('Height'),
                        dcc.Input(
                                id='height',
                                type='float',
                                placeholder='Enter in cms/feets'
                        )
                    ]),

                    html.P([
                        html.Label('Height Metric'),
                        dcc.Dropdown(
                                id='metric',
                                options=[#{'label': 'Meters', 'value':'mts'},
                                        {'label':'Centimeters', 'value':'cms'},
                                        #{'label':'Inches', 'value':'ins'},
                                        {'label':'Feets', 'value':'fts'}],
                                value = 'cms'

                        )
                    ], style={'width':'145px'}),

                    html.P([
                    html.Button(
                        id='bmi_submit',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':20}
                    )],style={ 'width':'10%'})

            ], style={'display':'inline-block', 'width':'15%', 'paddingLeft':'50px', 'verticalAlign':'Top'}),

            # create div to display BMI levels information
            html.Div(id='bmi_table',

                children = [generate_table(BMI_df),
                            html.P(id='bmi_result')],
                style={'display':'inline-block', 'width':'20%', 'paddingLeft':'50px', 'verticalAlign':'Top'}),

            # create div to capture inputs for Hip-Waist ratio calculation,
            html.Div([
                    html.H4('Waist to Hip ratio'),
                    #html.P('2.54 cms = 1 Inch'),
                    html.P([
                        html.Label('Waist (Inch)'),
                        dcc.Input(
                                id='waist',
                                type='float',
                                placeholder='measurement in Inches',
                        )]),

                    html.P([
                        html.Label('Hip (Inch)'),
                        dcc.Input(
                                id='hip',
                                type='float',
                                placeholder='measurement in Inches'
                        )
                    ]),

                    html.P([
                        html.Label('Gender'),
                        dcc.Dropdown(
                                id='gender',
                                options=[#{'label': 'Meters', 'value':'mts'},
                                        {'label':'Female', 'value':'female'},
                                        #{'label':'Inches', 'value':'ins'},
                                        {'label':'Male', 'value':'male'}],

                        )
                    ], style={'width':'145px'}),


                    html.P([
                    html.Button(
                        id='wth_submit',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':20}
                    )],style={ 'width':'10%'})

            ], style={'display':'inline-block', 'width':'17%', 'paddingLeft':'10px', 'verticalAlign':'Top'}),

            # create div to display HWR levels information
            html.Div(id='whr_table',

                children = [generate_table(WTH_df),
                            html.P(id='wth_result')],
                style={'display':'inline-block', 'width':'25%', 'paddingLeft':'50px', 'verticalAlign':'Top'}),

            #html.Div(generate_table_result(df))



            # create div to display the BMI and HWR results
            html.Div([
                dcc.Markdown('''
                    ***
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

            # Create a section for Insights questions
            html.Div([html.H3('Insights section')],
                    #className='content-container container-width',
                    style={'textAlign':'center', 'backgroundColor':'#76D7C4','width':'30%',
                            #'marginLeft':'460px',
                            'margin':'auto'}),

            html.Div([
                html.H6('''
                    Answer these questions and check your knowledge, reinforce/gain information.
                '''),
                html.H6('''Answer will appear in 9 seconds after the question appears''',style={'color': 'red'})
                ], style={#'paddingLeft':90,
                        'textAlignalign':'center','width':'30%',
                        #'marginLeft':'340px',
                        'margin':'auto','fontColor':'#F1948A'}),

            html.Div(id='insights_div',
                children = [#'Click "NEXT" to get started!'
                html.Label("One can skip breakfast?"),
                # dcc.Input(id='mother_birth', value=1952, type='number'),

                dcc.RadioItems(
                    id='i_questions',
                    options=[{'label': 'Yes', 'value': 'Yes'},
                             {'label': 'No', 'value': 'First insight: Never skip your Breakfast. "Now check the correct answer and click SUBMIT, then NEXT for more questions"'},
                             {'label': 'Maybe if busy', 'value': 'Maybe if busy'}],
                    value='First insight: Never skip your Breakfast. "Now check the correct answer and click SUBMIT, then NEXT for more questions"'
                )
                ],
                style={'width': '500px', 'paddingLeft':'5px',
                #'margin-right': '10px', 'margin-left': '10px', 'marginLeft':'420px',
                'text-align': 'left', 'margin':'auto', 'backgroundColor':'#F2D7D5'}),

            html.Div(dcc.Interval(id='interval-component',
                interval= 9000,
                n_intervals=0)),

            html.Div(id='feedback_div',
                    style={'width': '500px',
                    #'margin-right': '10px', 'margin-left': '10px', 'marginLeft':'420px',
                    'text-align': 'left', 'margin':'auto'}),
##
##            html.Div(
##            html.P([
##            html.Button(
##                id='insights_Sub',
##                n_clicks=0,
##                children='Submit',
##                style={'fontSize':20}
##            )],style={ 'width':'10%'})
##            , style={'display':'inline-block', 'width':'17%',
##                    'marginLeft':'430px',
##                    #'margin':'auto',
##                    'verticalAlign':'Top'}),

            html.Div(
            html.P([
            html.Button(
                id='insights_Q',
                n_clicks=0,
                children='Next',
                style={'fontSize':20}
            )],style={ 'width':'10%'})
            , style={'display':'inline-block', 'width':'17%',
                    'marginLeft':'580px',
                    #'margin':'auto',
                    'verticalAlign':'Top'}),

            html.Div([
                html.H6('''
                    If the answer given through feedback is not in the choices, correct answer will appear shortly. This is a little (5 Sec)
                    latency/delay issue.
                ''', style={'color': 'red'})
                ], style={#'paddingLeft':90,
                        'textAlignalign':'center','width':'30%',
                        #'marginLeft':'340px',
                        'margin':'auto','color':'#F1948A'}),

                # create div to start insights questions, aligned to left
                # display the question
                 # answers for the quesions

                # Give the correct answers for the questions

                # Provide the continues streak and highest streak information, aligned to right

            # Create a section display Motivatin quotes related to health
            html.Div([
                dcc.Markdown('''
                    ***
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),

            html.Div([html.H3('Motivation section')],
                    #className='content-container container-width',
                    style={'textAlign':'center', 'backgroundColor':'#76D7C4','width':'30%',
                            #'marginLeft':'460px',
                            'margin':'auto'}),

            html.Div([
                html.H6('''
                    Here are the motivation quotes which will provide the inspiration to get you started/keep going on the health mission
                ''')
                ], style={#'paddingLeft':90,
                        'textAlignalign':'center','width':'50%',
                        #'marginLeft':'260px'
                        'margin':'auto', 'fontColor':'#F1948A'}),

            html.Div(id='mot_div',
                     style={#'paddingLeft':90,
                        'textAlignalign':'center','width':'60%',
                        #'marginLeft':'270px'
                        'margin':'auto'}
                     ),

            html.Div([
            html.P([
            html.Button(
                id='mo_Q',
                n_clicks=0,
                children='Next',
                style={'fontSize':20}
            )],style={ 'width':'10%'})
            ], style={'display':'inline-block', 'width':'17%',
                    'marginLeft':'580px',
                    'marginTop':'10px',
                    #'margin':'auto',
                    'verticalAlign':'Top'}),
                # Create div to display the quotes
                    # create next button to call next quote
            html.Div([
                dcc.Markdown('''
                    ***
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),
    
            # Create div to give ending words towards the AIM for health
            html.Div([
                html.H6('''
                    Now that you are Aware of your health level and you have gained some insights by taking the questions given in the Insights section, and so you
                    have read the Motivation quotes.
                ''', style={'color':'#2980B9'}),
                html.H6('''
                    Hopefully this helped to set an AIM to improve/continue your fitness efforts. If you got satisfactory results using the Awareness section keep that
                    up, if not, nobody is stoping you from becoming fit.... So don't stop yourself.
                ''', style={'color':'#2980B9'})
                ], style={'paddingLeft':10,
                        'textAlignalign':'center','width':'50%',
                        #'marginLeft':'260px'
                        'margin':'auto', 'fontColor':'#2980B9', 'borderStyle':'dotted'}),
            html.Div([
                dcc.Markdown('''
                    ***
                '''.replace('  ',''), className='container',
                containerProps={'style':{'maxwidth':'300px','textAlign':'center'}})]),
])

# assinging layout to app
app.layout = layout

# Create Input and Output callbacks for the BMI and HWR section
@app.callback(
        Output('bmi_result', 'children'),
        [Input('bmi_submit','n_clicks')],
        [State('weight','value'),
         State('height','value'),
         State('metric','value')
        ])
def bmi_callback(click, weight, height, metric):

    if weight != '' and height != '' and metric != '':
        try:
            if metric == 'fts':
                feets = height[0]
                if len(height) > 1:
                    inches = height[2:]
                    meters = (0.3048 * float(feets)) + (0.0254 * float(inches))
                else:
                    meters = 0.3048 * float(feets)
            elif metric == 'cms':
                meters = 0.01 * float(height)

            BMI = round(float(weight)/(meters**2), 1)
            bmi_colors = ['orange','green','#FF6666','#FF3333','#FF0000','#CC0000']
            if BMI < 18.5:
                color = bmi_colors[0]
            elif BMI >= 40:
                color = bmi_colors[5]
            elif BMI >= 35:
                color = bmi_colors[4]
            elif BMI >= 30:
                color = bmi_colors[3]
            elif BMI >= 25:
                color = bmi_colors[2]
            elif BMI >= 18.5:
                color = bmi_colors[1]

            return html.P(BMI, style={'backgroundColor':color, 'textAlign':'center','fontSize':20,'width':'100px'})
            #return BMI
        except TypeError:
            return html.P("Enter required values", style={'backgroundColor':'#C0C0C0','width':'150px','textAlign':'center'})

@app.callback(Output('wth_result','children'),
              [Input('wth_submit','n_clicks')],
              [State('waist','value'),
               State('hip','value'),
               State('gender','value')])
def wth_callback(click, waist, hip, gender):
    if waist != '' and hip != '' and gender != '':
        try:
            wth_ratio = round(float(waist)/float(hip), 2)
            #return wth_ratio
            wth_colors = ['green','#FF3333','#FF0000']
            if gender == 'female':
                if wth_ratio >= 0.85:
                    color = wth_colors[2]
                elif wth_ratio >= 0.81:
                    color = wth_colors[1]
                elif wth_ratio <= 0.80:
                    color = wth_colors[0]
            elif gender == 'male':
                if wth_ratio >= 1:
                    color = wth_colors[2]
                elif wth_ratio >= 0.96:
                    color = wth_colors[1]
                elif wth_ratio <= 0.95:
                    color = wth_colors[0]

            return html.P(wth_ratio, style={'backgroundColor':color, 'textAlign':'center','fontSize':20,'width':'100px'})

        except TypeError:
            return html.P("Enter required values", style={'backgroundColor':'#C0C0C0', 'width':'150px', 'textAlign':'center'})


# Create Input and Ouput callback for insights section


    

@app.callback(
        Output('insights_div', 'children'),
        [Input('insights_Q','n_clicks')],
        #[State('i_questions','value')]
        )
def insights_next(click1):

    if d_dict == {}:
        return "Great going! you have completed all the questions. Come back later! for more....."
    # ran = np.random.randint(len(data))
    # while True:
    #     if ran in questions_count:
    #         ran = np.random.randint(len(data))
    #         #continue
    #     else:
    #         break
    global question_index
    question = d_dict.pop(question_order[question_index])
    #questions_count.append(ran)
    question_index += 1

    Q_label = question['Question']
    choices = [question['Answer'], question['W1'], question['W2']]
    global expected_answer
    expected_answer = question['Answer']
    #expected_answer.append(question['Answer'])
    #choice_2 = question['W1']
    #choice_3 = question['W2']
    choices = np.random.choice(choices, 3, replace=False)

#f_question = '{}: \n1. {}\n2. {}\n3. {}\n'.format(question['Question'],question['Answer'],question['W1'],question['W2'])

    next_question = (
    html.Label(Q_label),
    # dcc.Input(id='mother_birth', value=1952, type='number'),

    dcc.RadioItems(
        id='i_questions',
        options=[{'label': choices[0], 'value': choices[0]},
                 {'label': choices[1], 'value': choices[1]},
                 {'label': choices[2], 'value': choices[2]}],
        value=""
    ))

    return next_question
  


# def insights_sub(c1, click2, response):
#     if response == question['Answer']:
#         return '{}: {}\n{}'.format('correct',question['Question'], question['Answer'])
#     else:
#         return '{}: {}\n{}'.format('incorrect',question['Question'], question['Answer'])

@app.callback(
        Output('feedback_div', 'children'),
        [Input('interval-component','n_intervals')]
        )
def insights_interval(interval):
    return html.P(
                '{}: {}'.format('Answer',expected_answer),
                style={'backgroundColor':'#ACED76','fontSize':'16px'})

##@app.callback(
##        Output('feedback_div', 'children'),
##        [Input('insights_Sub','n_clicks')],
##        [State('i_questions','value')]
##        )
##def insights_callback(click2, response):
##    while response == '':
##        sleep(0.5)
##        
##    global expected_answer
##    if response == expected_answer:
##        return html.P(
##                    '{}: {}'.format('Correct', expected_answer),
##                    style={'backgroundColor':'#ACED76','fontSize':'16px'})
##    else:
##        return html.P(
##                    '{}: {}'.format('Incorrect', expected_answer),
##                    style={'backgroundColor':'#F87C6F','fontSize':'16px'})



# Create Input and Output callbacks for motivation quotes section
@app.callback(
        Output('mot_div', 'children'),
        [Input('mo_Q','n_clicks')],
        )
def motivation_callback(click):
    if m_dict == {}:
        return html.P('Great going! You have completed all the available quotes. Come back later! for more.....',
        style={#'paddingLeft':90,
            'backgroundColor': '#F2D7D5',
            'textAlign':'center','width':'60%',
            'margin':'auto', 'paddingDown':'10'#'marginLeft':'260px'
        })
    while True:
    	ran = np.random.randint(len(data))
    	if ran in mot_count:
            continue
    	else:
            quote = m_dict.pop(ran)
            mot_count.append(ran)
            return html.H4(quote,
                        style={#'paddingLeft':90,
                            'backgroundColor': '#F2D7D5',
                            'textAlign':'center','width':'60%',
                            'margin':'auto', 'paddingDown':'10'#'marginLeft':'260px'
                        })


app.css.append_css({'external_url': css})
#app.config['suppress_callback_exceptions']=True
#run the server
if __name__ == '__main__':
    app.runserver()
    #sess = Session()
    #sess.init_app(app)
