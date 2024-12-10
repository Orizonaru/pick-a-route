from flask import Flask, render_template, jsonify, request, current_app
import logging
import requests
from app.request_weather import RequestWeather

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api_key = 'qiLNhPlYwsQwGIOAdSB8XbXOD1m1tQGE'


@app.route('/')
def run():
    return render_template('index.html')


@app.route('/api/weather', methods=['POST'])
def get_weather():
    data = request.json
    city = data.get("city")

    if not city:
        return jsonify({"error": "Не указан город"}), 400

    weather_client = RequestWeather(api_key=api_key, language="ru-ru")

    try:
        autocomplete_results = weather_client.fetch_city_autocomplete(city)
        if not autocomplete_results:
            return jsonify({"error": "Город не найден"}), 404

        location_code = autocomplete_results[0]["Key"]
        forecast = weather_client.fetch_daily_forecast(forecast_days=5, location_code=location_code, include_details=True)

        return jsonify({"forecast": forecast})
    except Exception as e:
        return jsonify({"error": "Не удалось получить данные", "details": str(e)}), 500


@app.route('/api/weather/multiple', methods=['POST'])
def get_multiple_weather():
    data = request.json
    start_city = data.get("start_city")
    end_city = data.get("end_city")

    if not start_city or not end_city:
        return jsonify({"error": "Не указаны оба города"}), 400

    def weather_validation(temp_max, temp_min, wind_speed, rain_prob):
        if temp_max > 35 or temp_min < -10 or wind_speed > 50 or rain_prob > 80:
            return False
        else:
            return True

    weather_client = RequestWeather(api_key=api_key, language="ru-ru")

    def get_city_weather(city_name):
        autocomplete_results = weather_client.fetch_city_autocomplete(city_name)
        if not autocomplete_results:
            return None
        location_code = autocomplete_results[0]["Key"]
        forecast = weather_client.fetch_daily_forecast(forecast_days=1, location_code=location_code)[0]
        return {
            "name": city_name,
            "temp_max": forecast["temp_max"],
            "temp_min": forecast["temp_min"],
            "wind_speed": forecast["wind_speed"],
            "rain_probability": forecast["rain_prob"],
            "is_good": weather_validation(forecast["temp_max"], forecast["temp_min"], forecast["wind_speed"], forecast["rain_prob"])
        }

    start_city_data = get_city_weather(start_city)
    end_city_data = get_city_weather(end_city)

    if not start_city_data or not end_city_data:
        return jsonify({"error": "Не удалось получить данные для одного из городов"}), 500

    return jsonify({"start_city": start_city_data, "end_city": end_city_data})


if __name__ == '__main__':
    app.run(debug=True)