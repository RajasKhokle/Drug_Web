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

#Create connection to the database
engine = create_engine('postgres://postgres:DataAdmin@127.0.0.1:5432/Capstone')

# Create App name
app = Flask(__name__)

# Load the Drug
def load_drug(drug):
    
    sql_string = '''SELECT sum(quantity),period FROM "Casptone_Tableau" WHERE TRANBNFCODE = '''+drug+ ' group by period '
    print(sql_string)
    df = pd.read_sql(sql_string,engine)
    df['dt'] = pd.to_datetime(df.period, format = '%Y%m',errors = 'coerce')
    ds=df['dt']                  # Column for datestamp in Prophet model
    y = df['sum']                # Column for timeseries in prohet model
    data_dict = {'ds':ds,'y':y}
    ts = pd.DataFrame(data_dict)
    ts.reset_index(inplace =True,drop =True)
    return(ts)
    
# fbprophet forecasting function
def prophetmodel(ts,forecast_period=12):
    # Train Test Split 
    train = ts[:-12]   # leave out last twelve points for testing 
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
        print(type(drug),engine)
        ts = load_drug(drug)
        print('drug loaded')
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
    
    
