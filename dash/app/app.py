import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

import flask

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

# load our data
mtcars = pd.read_csv('mtcars.csv',
                    dtype={'cyl': str,
                          'am': np.float64})

# create and fit a one-hot encoder--we'll want to reuse this in the app as well
cyl_enc = OneHotEncoder(categories = 'auto', sparse=False)
cyl_enc.fit(mtcars['cyl'].values.reshape(-1,1))

y = mtcars['mpg']
# we need to concatenate the one-hot (dummy) encoded values with
# the values from mtcars
X = np.concatenate(
    (mtcars[['disp', 'qsec', 'am']].values, 
     cyl_enc.transform(mtcars['cyl'].values.reshape(-1,1))),
     axis=1)

# fit our regression model
fit = LinearRegression()
fit.fit(X=X, y=y)

def preds(fit, cyl_enc, disp, qsec, am, cyl):
    # construct our matrix
    X = np.concatenate(
        (np.array([[disp, qsec, am]]),
         cyl_enc.transform([[cyl]])),
         axis=1)
    # find predicted value
    pred = fit.predict(X)[0]
    # return a rounded string for nice UI display
    return str(round(pred, 2))


# load the resuired modules


# create an instance of a dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = 'Predicting MPG'

# dash apps are unstyled by default
# this css I'm using was created by the author of Dash
# and is the most commonly used style sheet
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# I compute these up front to avoid having to
# calculate thes twice
unq_cyl = mtcars['cyl'].unique()
unq_cyl.sort() # so it's in a nice order
opts_cyl = [{'label': i, 'value': i} for i in unq_cyl]


app.layout = html.Div([
       
        html.H5('Displacement (in cubic inches):'),
        html.Br(), html.Br(),
        daq.Slider(
            id='input-disp',
            min=np.floor(mtcars['disp'].min()),
            max=np.ceil(mtcars['disp'].max()),
            step=.5,
            dots=False,
            handleLabel={"showCurrentValue": True,"label": "Value"},
            value=np.floor(mtcars['disp'].mean())),

        html.H5('Quarter mile time:'), 
        html.Br(),
        daq.Slider(
            id='input-qsec',
            min=np.floor(mtcars['qsec'].min()),
            max=np.ceil(mtcars['qsec'].max()),
            dots=False,
            handleLabel={"showCurrentValue": True,"label": "Value"},
            step=.25,
            value=np.floor(mtcars['disp'].mean())),
        
        html.H5('Number of cylinders:'),
        dcc.RadioItems(
            id='input-cyl',
            options=opts_cyl,
            value=opts_cyl[0].get('value'),
            labelStyle={'display': 'inline-block'}),

        daq.ToggleSwitch(
            id='input-am',
            label='Has manual transmission',
            value=False),

        html.H2(id='output-prediction')
])

# callback will watch for changes in inputs and re-execute when any
# changes are detected. 
@app.callback(
    dash.dependencies.Output('output-prediction', 'children'),
    [
        dash.dependencies.Input('input-disp', 'value'),
        dash.dependencies.Input('input-qsec', 'value'),
        dash.dependencies.Input('input-cyl', 'value'),
        dash.dependencies.Input('input-am', 'value')])
def callback_pred(disp, qsec, cyl, am):
    # pass values from the function on to our prediction function
    # defined in setup
    pred = preds(fit=fit, 
                 cyl_enc=cyl_enc, 
                 disp=disp, 
                 qsec=qsec, 
                 am=np.float64(am), 
                 cyl=cyl)
    # return a string that will be rendered in the UI
    return "Predicted MPG: {}".format(pred)

app.config.supress_callback_exceptions = True
app.config.update({
    # as the proxy server will remove the prefix
    'routes_pathname_prefix': ''

    # the front-end will prefix this string to the requests
    # that are made to the proxy server
    , 'requests_pathname_prefix': ''
})

# for running the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
