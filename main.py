from flask import Flask, request
from flask_restful import Resource, Api
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
#from dash import html, dcc
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import dash_bootstrap_components as dbc
from dash import State
from flask import Flask
import flask_restful
from flask_restful import Resource, Api
import datetime



def serve_layout():
    return html.Div(style = {'bckgroundColor': "#000000"},children = [
                           html.H1(children="""
                              Smart Home""",
                              style={
                                  'textAlign': 'center',
                                  #'color': ""
                                  }),
                            #---------------------------------------------------
                            html.A(
                                href="https://mail.google.com/mail/",children=[
                                    html.H6(children="Mohammed Hammoud  ",
                                     style={
                                         'textAlign': 'right',
                                         #'color': themes['text']
                                  })
                                  ]
                            ),

                           #---------------------------------------------------
                            html.Div(children = 'Data from labview ',
                                    style = {
                                       'textAlign': 'center',
                                       'color': themes['text']
                                   }),

                            html.Div(dcc.Input(id='input-on-submit', type='text')),
                            html.Br(),
                            html.Button('Submit', id='submit-val', n_clicks=0),
                            html.Div(id='container-button-basic',children='Enter a value and press submit'),
                            #---------------------------------------------------

                          dcc.Tabs([

                                #---------------------------------------------------
                                dcc.Tab(label=SECTION['var'],style={'background': "grey"},children=[
                                            dcc.Graph(id="g1",
                                                animate = True,
                                                figure={}
                                                        )]),
                                dcc.Tab(label=SECTION['Temerature'],style={'background': "grey"},children=[
                                            dcc.Graph(
                                                figure={
                                                    'data': [
                                                        {'x': list(range(25)), 'y': list(random.sample(range(0,50), 25)),'marker': {'size': 12},'mode':'lines+markers','name': 'Room1'},
                                                        {'x':list(range(25)), 'y':  list(random.sample(range(0,50), 25)),'marker': {'size': 12},'mode':'lines+markers', 'name': 'Room2'}
                                                        ],
                                                    'plot_bgcolor': "#000000" ,#themes['background'],
                                                    'paper_bgcolor': themes['background'],
                                                    'font': {
                                                        'color': "#ff00ff"#themes['text']
                                                    }
                                                        })]),

                                #---------------------------------------------------
                                dcc.Tab(label=SECTION['Humidity'],style={'background': "grey"},children=[
                                            dcc.Graph(
                                                figure={
                                                    'data': [
                                                        {'x': list(range(25)), 'y': list(random.sample(range(0, 50), 25)),'marker': {'size': 12},'mode':'lines+markers','name': 'Room1'},
                                                        {'x':list(range(25)), 'y':  list(random.sample(range(0, 50), 25)),'marker': {'size': 12},'mode':'lines+markers', 'name': 'Room2'}
                                                        ],
                                                    'plot_bgcolor': "#000000" ,#themes['background'],
                                                    'paper_bgcolor': "#000000",
                                                    'font': {
                                                        'color': "#ff00ff"#themes['text']
                                                    }
                                                        })]),
                                dcc.Tab(label="Test_Auto_update_1Sec",style={'background': "grey"},children=[
                                    dcc.Graph(id='live-graph', animate=True),
                                    dcc.Interval(
                                        id='graph-update',
                                        interval=10000 )
                                ])
                        ])
                        ])

SECTION = {"Temerature":"temperature..",
            "Humidity":"humidity..",
            "var":"variable"
            }

X = deque(maxlen=50)
X.append(1)
Y = deque(maxlen=50)
Y.append(1)

X1 = deque(maxlen=50)
Y1 = deque(maxlen=50)
themes = {
    'background': '#ffffff',
    'text': '#ffffff'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

external_stylesheets = [dbc.themes.BOOTSTRAP] #https://bootswatch.com/default/
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#--------------------------------------------------------------------------------------------------------
server = Flask(__name__)
api = Api(server)

app = dash.Dash(server=server, external_stylesheets = external_stylesheets, update_title=None)#, url_base_pathname='/dashboard/')
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

sensors_val_last = {'Temp1':21, 'Temp2':22, 'Temp3':23}

class sensor(Resource):
    def get(self, sensor_id):
        if sensor_id in sensors_val_last.keys():
            return {sensor_id: sensors_val_last[sensor_id]}
        else:
            return "Sorry"
        
    def post(self, sensor_id):
        #new_file=open("newfile.txt",mode="w",encoding="utf-8")
        #new_file.write("Writing to a new file\n")
        #new_file.close()
        sen_id, val = sensor_id.split('=')
        sensors_val_last[sen_id] = float(val)
        
        return {sen_id: sensors_val_last[sen_id]}

api.add_resource(sensor, '/<string:sensor_id>')

app.layout = serve_layout()
#--------------------------------------------------------------------------------------------------------
@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    global sensors_val_last, X, Y
    #X.append(datetime.datetime.now())
    X.append(X[-1]+1)
    Y.append(sensors_val_last["Temp1"])
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return  {'data': [data],
            'layout':go.Layout(
            title="Sensor_output",
            plot_bgcolor="#FFF",  # Sets background color to white
            xaxis=dict(
                    range=[min(X),max(X)],
                    title="time",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False,  # Removes X-axis grid lines
                    showspikes=True, # Show spike line for X-axis
                    # Format spike
                    spikethickness=2,
                    spikedash="dot",
                    spikecolor="#999999",
                    spikemode="across",
                    # Adjust click behavior
                    #itemclick="toggleothers",
                    #itemdoubleclick="toggle",
                ),
            yaxis=dict(
                    range=[min(Y),max(Y)],
                    title="value",  
                    linecolor="#BCCCDC",  # Sets color of Y-axis line
                    showgrid=False,  # Removes Y-axis grid lines    
                )
            )
           }

@app.callback(
    [Output('container-button-basic', 'children'),
    Output('g1', 'figure')],
    [Input('submit-val', 'n_clicks'),],
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    global X1,Y1
    #X.append(X[-1]+1)
    X1.append(datetime.datetime.now())
    #X.append(1)
    tmp = int(random.randint(0,n_clicks))
    Y1.append(tmp)
    data = plotly.graph_objs.Scatter(
            x=list(X1),
            y=list(Y1),
            name='Scatter',
            mode= 'lines+markers'
            )
    fig =  {'data': [data],
            'layout':go.Layout(
            title="Sensor_output",
            plot_bgcolor="#FFF",  # Sets background color to white
            xaxis=dict(
                    range=[min(X1),max(X1)],
                    title="time",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False,  # Removes X-axis grid lines
                    showspikes=True, # Show spike line for X-axis
                    # Format spike
                    spikethickness=2,
                    spikedash="dot",
                    spikecolor="#999999",
                    spikemode="across",
                    # Adjust click behavior
                    #itemclick="toggleothers",
                    #itemdoubleclick="toggle",
                ),
            yaxis=dict(
                    range=[min(Y1),max(Y1)],
                    title="value",  
                    linecolor="#BCCCDC",  # Sets color of Y-axis line
                    showgrid=False,  # Removes Y-axis grid lines    
                )
            )
           }

    txt = '"{}" and the button has been clicked {} times'.format(value,n_clicks)
    return txt, fig

app.run_server()

