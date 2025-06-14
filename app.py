from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load and prepare data
df = pd.read_csv('cuaca_indonesia.csv')

# Encode labels
le = LabelEncoder()
df['label'] = le.fit_transform(df['weather'])

# Feature & target
X = df[['precipitation', 'temp_max', 'wind']]
y = df['label']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        precipitation = float(request.form['precipitation'])
        temp_max = float(request.form['temp_max'])
        wind = float(request.form['wind'])

        features = np.array([[precipitation, temp_max, wind]])
        prediction = model.predict(features)
        weather_pred = le.inverse_transform(prediction)[0]

        return jsonify({'prediction': f"Perkiraan cuaca: {weather_pred}"})
    except Exception as e:
        return jsonify({'prediction': f"Terjadi kesalahan: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
