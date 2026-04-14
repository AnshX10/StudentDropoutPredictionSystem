# predictions/utils.py
import os
import joblib
import logging
import numpy as np
from django.conf import settings

logger = logging.getLogger(__name__)

def predict_student_risk(academic_record):
    model_path = os.path.join(settings.BASE_DIR, 'predictions', 'ml_models', 'dropout_model.pkl')
    
    try:
        # Attempt to load the Machine Learning model
        model = joblib.load(model_path)
        features = np.array([[
            academic_record.attendance_percentage,
            academic_record.sgpa,
            academic_record.cgpa,
            academic_record.backlogs_current
        ]])
        
        prediction_class = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Store as a percentage (e.g., 85.5)
        risk_score = float(max(probabilities)) * 100.0 
        
        if prediction_class == 0: risk_level = 'LOW'
        elif prediction_class == 1: risk_level = 'MEDIUM'
        else: risk_level = 'HIGH'
            
        return risk_level, risk_score

    except Exception as exc:
        logger.warning(f"ML model unavailable. Using heuristic fallback. Error: {exc}")
        
        # --- RULE-BASED FALLBACK LOGIC ---
        attendance = academic_record.attendance_percentage
        sgpa = academic_record.sgpa
        backlogs = academic_record.backlogs_current
        
        # Calculate a rough risk percentage
        score = max(0.0, 1.0 - (sgpa / 10.0)) * 0.6 + min(1.0, backlogs / 5.0) * 0.4
        risk_score = round(score * 100.0, 2)
        
        if sgpa < 5.0 or backlogs >= 4 or attendance < 50.0:
            risk_level = 'HIGH'
        elif sgpa < 7.0 or backlogs >= 2 or attendance < 75.0:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
            
        return risk_level, risk_score