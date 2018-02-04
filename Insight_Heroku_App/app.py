import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plotly import graph_objs as go
import pandas as pd
import os
from flask import Flask
import pickle as pk
import base64

### ----- Reference for updating app.py ----- ###
# git status # view the changes
# git add .  # add all the changes
# git commit -m 'a description of the changes'
# git push heroku master

### ----- GET INFO ----- ###

## Load pickle data ##
ridge = pk.load(open('ridge.pkl','rb'))
insighttable = pk.load(open('insighttable.pkl','rb'))
headshot = 'headshot.png'
encoded_headshot = base64.b64encode(open(headshot, 'rb').read())
run = 'running.gif'
encoded_run = base64.b64encode(open(run, 'rb').read())

## Make table of insights ##
def generate_table(dataframe, max_rows=30):
    return html.Table(
        ## Header ##
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        ## Body ##
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
        style={
		'padding': '10',
        'padding-top': '5',
		'padding-bottom': '10',
		'fontSize': 18}
    )
Z = generate_table(insighttable)

## Plotly: plot embed urls ##

urls = {
    'Daily': 'https://plot.ly/~dalfego/84.embed',
	'Weekly': 'https://plot.ly/~dalfego/28.embed',
    'Monthly': 'https://plot.ly/~dalfego/30.embed'}

init_key, init_val = next(iter(urls.items()))

### ----- APP SETUP ----- ###

## Initialize Dash objects ##
app = dash.Dash()
server = app.server
app.title = 'Run With it!'

## Suppress warning for multipages ##
app.config.suppress_callback_exceptions = True

## Define dropdown whose options are embed urls ##
dd = dcc.Dropdown(      
    id='dropdown',
    options= [{'label': k, 'value': v} for k, v in urls.items()])

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

## Embedded plot element whose `src` parameter will
# be populated and updated with dropdown values ##

plot = html.Iframe(
    id='plot',
    style={'border': 'none', 'width': '100%', 'height': 500},
    src=init_val)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


## ----- HOME PAGE LAYOUT / RUN PREDICTOR -----##

index_page = html.Div(children=[
	
	## Title ##
	html.Div([
		html.Div([
			html.Div([
				html.H1('Run With It!'),
			], 
			className="nine columns padded"),
			html.Div([
				html.H5(
				  [html.Span('Insight Data Science Consulting Project', style={'opacity': '0.5'})]),
				html.H6('by David Alfego')
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'})],
        className="row gs-header gs-text-header")]),
    
    html.Div([
    	html.H5('Menu'),
    	html.Div([
    		dcc.Link('Run Predictor', href='/')],
    		className='two columns'),
    	html.Div([
    		dcc.Link('Health Insights', href='/page-3')],
    		style={'color': '#b1efb3'},
    		className='two columns'),
    	html.Div([
    		dcc.Link('About Me', href='/page-2')],
    		className='two columns'),
    	html.Hr()]
    	),
    
    html.Img(src='data:image/png;base64,{}'.format(encoded_run.decode())
	  ),
	
	## Header ##
	html.Div([
		html.Div([
			html.H6('How long should you run today? Fill in your metrics:',
			  className="gs-header gs-text-header padded",
			  style={'color': '#7F90AC','fontSize':14}),
	], className="twelve columns padded")
	]),
	
	## Run Predictor ##
    html.Div(children=[
    	
        html.Div(children=[
            html.Label('What is your step goal today?'),
            dcc.Input(
                value='10000', 
                id='steps')]),

        html.Div(children=[
            html.Label('What is your projected average heart rate? (bpm)'),
            dcc.Input(
                value='75',
                id='hr')]),

        html.Div(children=[
            html.Label('What is your weight? (lbs.)'),
            dcc.Input(
                value='155',
                id='weight')]),        

        html.Div(children=[
            html.Label('What is your body fat percentage?'),
            dcc.Input(
                value='20',
                id='bf')]),
        
        html.Div(children=[
            html.Label('What is your sleep goal? (hours)'),
            dcc.Input(
                value='8',
                id='sleep')]),

        html.Div(children=[
            html.Label('What is your running pace per mile?'),
            dcc.Dropdown(
                options=[
				  	{'label': '4', 'value': '4'},
				  	{'label': '5', 'value': '5'},
				  	{'label': '6', 'value': '6'},
				  	{'label': '7', 'value': '7'},
				  	{'label': '8', 'value': '8'},
				  	{'label': '9', 'value': '9'},
				  	{'label': '10', 'value': '10'},
				  	{'label': '11', 'value': '11'},
				  	{'label': '12', 'value': '12'},
				  	{'label': '13', 'value': '13'},
				  {'label': '14', 'value': '14'}],
				  id='pace_min',
				  placeholder = 'min',
				  value='')],
            className='five columns',
            style={'width': '100%', 'margin-left': 0, 'margin-top': 20, 'margin-bottom': 20}),
        
        html.Div(children=[
            dcc.Dropdown(
                options=[
				  	{'label': '00', 'value': '0'},
				  	{'label': '05', 'value': '5'},
				  	{'label': '10', 'value': '10'},
				  	{'label': '15', 'value': '15'},
				  	{'label': '20', 'value': '20'},
				  	{'label': '25', 'value': '25'},
				  	{'label': '30', 'value': '30'},
				  	{'label': '35', 'value': '35'},
				  	{'label': '40', 'value': '40'},
				  	{'label': '45', 'value': '45'},
				  	{'label': '50', 'value': '50'},
				  {'label': '55', 'value': '50'}],
				  id='pace_sec',
				  placeholder = 'sec',
				  value='')],
            className='five columns',
            style={'width': '100%', 'margin-left': 0, 'margin-top': 20, 'margin-bottom': 20})
    	],

        className='six columns',
        style={'background-color':'LightGray', 'padding': '20px'}
        ),


    ## Predictions title ##
    html.Div(children=[
        html.H3('Your predicted running time:', 
          style={'text-align': 'center'}),
        html.Div(
            id='prediction',
            style={'text-align': 'center'})
        ],
        className='six columns',
        style={'background-color':'#f4f7cd', 'padding': '20px'}),

    ## Footer ##
    html.Div(children=[
            html.Hr(),
            html.H5(children='David Alfego',
                style={'font-style': 'italic'}),
            html.H1(' ')],
        className='twelve columns',
        style={'text-align': 'center', 'padding': '50'}),

],	
## Sizing the overall page / font ##
style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'fontSize': '16',
        'padding': '40',
        'padding-top': '20',
    	'padding-bottom': '50'},
)

## ----- HOME PAGE CALLBACKS ----- ##

## Predictor algorithm ##
@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    [dash.dependencies.Input('steps', 'value'),
     dash.dependencies.Input('hr', 'value'),
     dash.dependencies.Input('weight', 'value'),
     dash.dependencies.Input('bf', 'value'),
     dash.dependencies.Input('sleep', 'value'),
     dash.dependencies.Input('pace_min', 'value'),
     dash.dependencies.Input('pace_sec', 'value')])
def model_relat(steps, hr, weight, bf, sleep, pace_min, pace_sec): 
  
    steps = int(steps)
    hr = int(hr)
    weight = int(weight)
    bf = int(bf)
    sleep = int(sleep)
    run_distance = 0
    run_distance = int(run_distance)
    pace_min = int(pace_min)
    pace_sec = int(pace_sec)
    
    goals = pd.DataFrame([steps, hr, weight, bf, sleep, run_distance])
    goals = goals.transpose()
         
    prediction = ridge.predict(goals)
    prediction = int(prediction[0])-15
    pred2 = divmod(prediction, 60)
    prediction_hrs = pred2[0]
    prediction_min = pred2[1]
    
    pace_convert = pace_min + pace_sec/60
    distance = prediction/pace_convert
    distance = round(distance,1)
    
    if prediction < 59:
      pred_output_str = '{} minutes'.format(prediction)
      pace_output_str = 'At your pace, that will be: {} miles'.format(distance)
      children = [html.H4(pred_output_str), html.H4(pace_output_str)]
      return children
    elif prediction >= 60 & prediction_hrs < 1:
      pred_output_str = '{} hour and {} minutes'.format(prediction_hrs, prediction_min)
      pace_output_str = 'At your pace, that will be: {} miles'.format(distance)
      children = [html.H4(pred_output_str), html.H4(pace_output_str)]
      return children
    elif prediction >= 60 & prediction_hrs > 1:
      pred_output_str = '{} hours and {} minutes'.format(prediction_hrs, prediction_min)
      pace_output_str = 'At your pace, that will be: {} miles'.format(distance)
      children = [html.H4(pred_output_str), html.H4(pace_output_str)]
      return children

## ----- PAGE 2 LAYOUT ----- ##

page_2_layout = html.Div([
    ## Title ##
	html.Div([
		html.Div([
			html.Div([
				html.H1('Run With It!')
			], 
			className="nine columns padded"),
			
			html.Div([
				html.H5(
				  [html.Span('Insight Data Science Consulting Project', style={'opacity': '0.5'})]),
				html.H6('by David Alfego')
                ], 
                className="three columns gs-header gs-accent-header padded", style={'float': 'right'})],
        className="row gs-header gs-text-header"
      )]),
    
    ## Menu ##
    html.Div([
    	html.H5('Menu'),
    	html.Div([
    		dcc.Link('Run Predictor', href='/')],
    		className='two columns'),
    	html.Div([
    		dcc.Link('Health Insights', href='/page-3')],
    		style={'color': '#b1efb3'},
    		className='two columns'),
    	html.Div([
    		dcc.Link('About Me', href='/page-2')],
    		className='two columns'),
    	html.Hr()]
    	),
    
    ## About Me Section ##
	html.H1('About Me'),
	html.Hr(),
	html.Div([
		html.Div([
			html.Div([
				html.Img(src='data:image/png;base64,{}'.format(encoded_headshot.decode()),
				  className='two columns',
				  style={'margin': 'auto'}, 
				  ),

				html.P('David Alfego is currently a Health Data Science Fellow with Insight Data \
				  Science in Boston, MA. He has a Ph.D. in Biomedical Science from Drexel \
				  University, where he researched metabolic \
				  stress responses in cellular aging through computational simulations \
				  and next-generation sequencing analysis. As a consultant for Ongo Science, \
				  a company that aims to provide personalized health insights from wearable tech, \
				  David (an avid runner) created a tool to help users reach \
				  their health goals through running.', style={'text-align': 'left', 'padding': '40px', 'padding-top': '30'},
				  className='ten columns')
			  ])
			]),
		],
		className='twelve columns'),
	html.Div([
		html.Div([
			html.A("Connect with David on LinkedIn", href='http://www.linkedin.com/in/davidalfego', target='_blank',
		className="twelve columns padded", style={'text-align': 'center'})])
	]),
	
	html.Div([
		html.Div([
			html.H6('Check out his presentation!',
			  className="gs-header gs-text-header padded",
			  style={'color': '#7F90AC'}),
	], 
	className="twelve columns padded")]
		),
	
	html.Div([
		html.Iframe(src="https://docs.google.com/presentation/d/e/2PACX-1vRMuXmgEnj96iIR-pi8wH5Plx61UKvE9QUzsghD0MPfuuagxTG4o74rrAcFi33ocCwpmiYwuo9dMiDc/embed?start=false&loop=false&delayms=10000",
		className = 'twelve columns',  
		style={'border': 'none', 'width': 950, 'height': 500, 'allowfullscreen' : 'true','mozallowfullscreen':'true', 'webkitallowfullscreen':'true', 'float': 'center',
		'padding-left':'200px'}),
	
		html.Div([
		html.A("Or follow this link for fullscreen", href='https://goo.gl/rC6x6v', target='_blank',className="twelve columns padded", style={'text-align': 'center'}),	
		]),
	]),
    
    ## Footer ##
    html.Div(children=[
				html.Hr(),
				html.H6(children='David Alfego',
				  style={'font-style': 'italic'}
				  ),
            	html.H1(' '),
    			html.Div(id='page-2-content'
    			  ),
				html.Br(),
				dcc.Link('Return Home', href='/'),
				html.Br(),
				dcc.Link('Health Insights', href='page-3')],
            		className='twelve columns',
            		style={'text-align': 'center', 'padding': '50'}
            		),
],
## Sizing the overall page / font ##
style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'fontSize': '16',
        'padding': '40',
        'padding-top': '20',
    	'padding-bottom': '50'},
    	)

### ----- PAGE 2 CALLBACKS ----- ###

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
      return page_2_layout
    elif pathname == '/page-3':
      return page_3_layout
    else:
      return index_page
        
### ----- PAGE 3 LAYOUT ----- ###        

page_3_layout = html.Div([
	
	## Title ##
	html.Div([
		html.Div([
			html.Div([
				html.H1('Run With It!')
			], className="nine columns padded"),
			html.Div([
				html.H5(
				  [html.Span('Insight Data Science Consulting Project', style={'opacity': '0.5'})]),
				html.H6('by David Alfego')
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'})],
        className="row gs-header gs-text-header")]
        ),
    
    ## Menu ##
    html.Div([
    	html.H5('Menu'),
    	html.Div([
    		dcc.Link('Run Predictor', href='/')],
    		className='two columns'),
    	html.Div([
    		dcc.Link('Health Insights', href='/page-3')],
    		style={'color': '#b1efb3'},
    		className='two columns'),
    	html.Div([
    		dcc.Link('About Me', href='/page-2')],
    		className='two columns'),
    	html.Hr()]
    	),
    
    html.Img(src='data:image/png;base64,{}'.format(encoded_run.decode(),
				  )
	  ),
	
	## Summaries ##
    
	html.Div([
		html.Div([
			html.H6('Please select a summary type for User 1:',
			  className="gs-header gs-text-header padded",
			  style={'color': '#7F90AC'}),
	], className="twelve columns padded")]),
	
	html.Div(children=[dd, plot]),
	
	## Header ##
	html.Div([
		html.Div([
			html.H6('How are your overall metrics correlated? Press the button:',
			  className="gs-header gs-text-header padded",
			  style={'color': '#7F90AC'}),
	], className="twelve columns padded")]),
	
	## Insight Button ##
	html.Button('Generate Insights!', id='button',style={
		'align': 'center',
		'fontSize': 14}),
	html.H3(id='target'),

	## Footer ##
    html.Div(children=[
				html.Hr(),
				html.H6(children='David Alfego',
				  style={'font-style': 'italic'}
				  ),
            	html.H1(' '),
    			html.Div(id='page-2-content'
    			  ),
				html.Br(),
				dcc.Link('Return Home', href='/'),
				html.Br(),
				dcc.Link('About Me', href='page-2'
				  )],
            		className='twelve columns',
            		style={'text-align': 'center', 'padding': '50'}
            		),

],	

## Sizing the overall page / font ##
style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'fontSize': '16',
        'padding': '40',
        'padding-top': '20',
    	'padding-bottom': '50'},
)

### ----- PAGE 3 CALLBACKS ----- ###

## update `src` parameter on dropdown select action ##
@app.callback(
    Output('plot', 'src'),
    [Input('dropdown', 'value')])
def update_plot_src(input_value):
    return input_value

## Button callback ##
@app.callback(
    dash.dependencies.Output('target','children'),
    [dash.dependencies.Input('button','n_clicks')]) 
def update_output(n_clicks):
  threshold =0
  if(n_clicks>threshold):
  	threshold=threshold+1
  	return   	html.H4(children='Personalized Health Insights'), Z
  	

    
### ----- TEMPLATE ----- ###

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


### ----- MAIN ----- ###

if __name__ == '__main__':

    app.run_server(debug=True)