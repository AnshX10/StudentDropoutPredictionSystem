# predictions/utils.py
import os
import joblib
import numpy as np
from django.conf import settings

def predict_student_risk(academic_record):
    # 1. Load the saved model
    model_path = os.path.join(settings.BASE_DIR, 'predictions', 'ml_models', 'dropout_model.pkl')
    model = joblib.load(model_path)
    
    # 2. Extract features from the academic record
    features = np.array([[
        academic_record.attendance_percentage,
        academic_record.sgpa,
        academic_record.cgpa,
        academic_record.backlogs_current
    ]])
    
    # 3. Make prediction
    # predict() gives the class (0, 1, or 2)
    # predict_proba() gives the percentage/confidence score of that prediction
    prediction_class = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Calculate the max confidence score (e.g., 0.85 -> 85%)
    risk_score = float(max(probabilities))
    
    # Map ML output to our database choices
    if prediction_class == 0:
        risk_level = 'LOW'
    elif prediction_class == 1:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'HIGH'
        
    return risk_level, risk_score