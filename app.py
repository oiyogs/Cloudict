from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '0441aae10855a19beaa714221628d566'  # Ganti dengan API Key Anda
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

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

if __name__ == '__main__':
    app.run(debug=True)
