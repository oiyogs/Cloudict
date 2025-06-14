from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load model dan label encoder
model = joblib.load('model_cuaca.pkl')
le = joblib.load('label_encoder.pkl')

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
