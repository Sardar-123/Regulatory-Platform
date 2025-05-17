#model_prediction.py

import joblib
import pandas as pd
import json

def load_model_and_encoders():
    rf_model = joblib.load('data/models/dora_compliance_model.pkl')
    label_encoders = joblib.load('data/encoders/label_encoder.pkl')
    one_hot_columns = joblib.load('data/encoders/one_hot_encoder.pkl')
    return rf_model,label_encoders, one_hot_columns

with open('data/weights/application_weights.json', 'r') as file:
    weights = json.load(file)

def predict_compliance_score(model, input_data, app_name, weights):
    max_possible_score = sum(weights[app_name].values()) * 3
    raw_score = model.predict(input_data)[0]
    return (raw_score / max_possible_score) * 100


