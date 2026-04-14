# train_dummy_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Create some dummy academic data
# Features:[Attendance(%), SGPA, CGPA, Backlogs]
# Labels (Risk Level): 0 = Low, 1 = Medium, 2 = High
data = {
    'attendance':[95, 88, 75, 45, 60, 90, 30, 80, 50, 98],
    'sgpa':[9.0, 8.5, 6.5, 4.0, 5.5, 8.0, 3.5, 7.0, 4.5, 9.5],
    'cgpa':[8.8, 8.4, 6.8, 4.2, 5.8, 8.1, 3.8, 7.2, 4.8, 9.2],
    'backlogs':[0, 0, 1, 4, 2, 0, 5, 1, 3, 0],
    'risk_level':[0, 0, 1, 2, 1, 0, 2, 0, 2, 0] 
}

df = pd.DataFrame(data)
X = df[['attendance', 'sgpa', 'cgpa', 'backlogs']]
y = df['risk_level']

# 2. Train the Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Save the trained model to our predictions app!
save_path = os.path.join('predictions', 'ml_models', 'dropout_model.pkl')
joblib.dump(model, save_path)
print(f"✅ Model successfully trained and saved to {save_path}")