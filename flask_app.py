# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:53:28 2019

@author: Rajas Khokle
Purpose: Python Flask Restful endpoint for predicting the demand forecasting
"""
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
from sqlalchemy import create_engine
from fbprophet import Prophet
import os
import warnings# Suppress warnings
warnings.filterwarnings("ignore")
import logging # Suppress Logs
logging.getLogger().setLevel(logging.CRITICAL)

#Create connection to the database
engine = create_engine('postgres://postgres:raj_drug_2019@127.0.0.1:5432/diabetes')

# Create App name
app = Flask(__name__)

# Load the Drug
def load_drug(drug):
    
    sql_string = '''SELECT sum(quantity),period FROM "df" WHERE TRANBNFCODE = '''+drug+ ' group by period '
    #print(sql_string)
    df = pd.read_sql(sql_string,engine)
    df['dt'] = pd.to_datetime(df.period, format = '%Y%m',errors = 'coerce')
    ds=df['dt']                  # Column for datestamp in Prophet model
    y = df['sum']                # Column for timeseries in prohet model
    data_dict = {'ds':ds,'y':y}
    ts = pd.DataFrame(data_dict)
    ts.reset_index(inplace =True,drop =True)
    return(ts)
    
# Suppress the output from prophet from pystan
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

# used like
# with suppress_stdout_stderr():
#     p = Propet(*kwargs).fit(training_data)
    
# fbprophet forecasting function
def prophetmodel(ts,forecast_period=12):
    # Train Test Split 
    train = ts[:-12]   # leave out last twelve points for testing 
    with suppress_stdout_stderr():
        model = Prophet()
        model.fit(train)
    future = model.make_future_dataframe(periods=forecast_period,freq='M') 
    forecast = model.predict(future)
    return(forecast)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/demand/', methods=['GET'])

def predict():
    try:
        drug = request.args.get('text')
        drug= "'"+drug+"'"
        #print(type(drug),engine)
        ts = load_drug(drug)
        #print('drug loaded')
        forecast = prophetmodel(ts)
        forecast = forecast.iloc[-1]
        demand = list(forecast)
        return jsonify(demand)
    except:
        response = jsonify(drug)
        response.status_code = 400
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777,debug=True)
    
    
