from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import joblib

app = Flask(__name__)

API_KEY = '0441aae10855a19beaa714221628d566'
model = joblib.load('model_cuaca.pkl')
le = joblib.load('label_encoder.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']

    try:
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()

        predictions = []
        used_days = set()
        
        for entry in data['list']:
            dt_txt = entry['dt_txt'].split()[0]
            if dt_txt in used_days:
                continue  # hanya ambil 1x per hari
            used_days.add(dt_txt)

            precipitation = entry.get('rain', {}).get('3h', 0.0)
            temp_max = entry['main']['temp_max']
            wind = entry['wind']['speed']

            features = np.array([[precipitation, temp_max, wind]])
            pred_label = model.predict(features)
            weather = le.inverse_transform(pred_label)[0]

            predictions.append({
                'date': dt_txt,
                'weather': weather
            })

            if len(predictions) == 5:
                break

        return jsonify({'forecast': predictions})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
