from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = '0441aae10855a19beaa714221628d566'  # Ganti dengan API Key Anda
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='Jakarta', type=str)
    url = f"{BASE_URL}?q={city}&units=metric&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'condition': data['weather'][0]['description'],
                'icon': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'City not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_forecast', methods=['GET'])
def get_forecast():
    city = request.args.get('city', default='Jakarta', type=str)
    url = f"{FORECAST_URL}?q={city}&units=metric&cnt=40&appid={API_KEY}"  # Get 40 data points (5 days * 8 data points per day)

    try:
        response = requests.get(url)
        data = response.json()

        if data['cod'] == '200':
            forecast_data = []
            day_data = {}

            # Proses data prediksi untuk 5 hari (setiap 3 jam interval)
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]  # Ambil tanggal saja (tanpa waktu)
                if date not in day_data:
                    day_data[date] = {'temperature': 0, 'count': 0, 'condition': item['weather'][0]['description'], 'icon': item['weather'][0]['icon']}

                # Hitung suhu rata-rata per hari
                day_data[date]['temperature'] += item['main']['temp']
                day_data[date]['count'] += 1

            # Ambil rata-rata suhu untuk setiap hari dan kumpulkan data untuk frontend
            for date, values in day_data.items():
                avg_temp = values['temperature'] / values['count']
                forecast_data.append({
                    'date': date,
                    'temperature': round(avg_temp, 1),
                    'condition': values['condition'],
                    'icon': f"https://openweathermap.org/img/wn/{values['icon']}.png"
                })

            return jsonify(forecast_data)
        else:
            return jsonify({'error': 'City not found for forecast'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
