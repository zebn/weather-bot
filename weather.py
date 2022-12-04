from flask import Flask, request, make_response, jsonify
import requests
import json
from geopy.geocoders import Nominatim
from OpenSSL import SSL
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/etc/letsencrypt/live/pokerbanking.ru/fullchain.pem', '/etc/letsencrypt/live/pokerbanking.ru/privkey.pem')

app = Flask(__name__)

API_KEY = '9d4e7fab3b84d65273c110579609c178'

@app.route('/')
def index():
    return 'Hello World!'

def results():
    req = request.get_json(force=True)

    action = req.get('queryResult').get('action')

    result = req.get("queryResult")
    parameters = result.get("parameters")

    if parameters.get('location').get('city'):
        geolocator = Nominatim(user_agent='weather-bot')
        location = geolocator.geocode(parameters.get('location').get('city'))
        lat = location.latitude
        long = location.longitude
        weather_req = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(lat, long, API_KEY))
        current_weather = json.loads(weather_req.text)['main']
        temp = round(current_weather['temp'] - 273.15)
        humd = current_weather['humidity']

    return {'fulfillmentText': 'La temperatura es {} celsius y humedad es {} prec'.format(str(temp),str(humd))}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="81",ssl_context=context)
