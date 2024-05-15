import joblib
import pandas as pd
from fraud.Fraud import Fraud
from flask import Flask, request, Response
import json

# loading model
model = joblib.load('trained_model/model_cycle1.joblib')

# initialize API
app = Flask(__name__)

@app.route('/fraud/predict', methods=['POST'])
def churn_predict():
    test_json = request.get_json()
   
    if test_json: 
        if isinstance(test_json, dict): # unique example
            test_raw = pd.DataFrame(test_json, index=[0])
            
        else: # multiple example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Instantiate Rossmann class
        pipeline = Fraud()
        
        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        
        # feature engineering
        df2 = pipeline.feature_engineering(df1)
        
        # data preparation
        df3 = pipeline.data_preparation(df2)
        
        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
#       data = json.loads(df_response)

#       Extract the "prediction" column
#       predictions = [entry["prediction"] for entry in data]
#       return predictions
        return df_response
        
        
    else:
        return Response('{}', status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run('0.0.0.0')