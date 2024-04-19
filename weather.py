import requests
from config import WEATHER_TOKEN

country = "BANGLADESH"
city = "Chandpur"

#URL = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={WEATHER_TOKEN}"
URL = "http://api.openweathermap.org/data/2.5/weather?" + f'q={city},{country}&appid={WEATHER_TOKEN}'

def weather():
    response = requests.get(URL)
    print(response)
    data = response.json()
    if data['cod'] == 200:
        weather_info = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        text = "Its " + str(weather_info) + ", temperature is " + str(int(temperature-273)) + " degree celsius and humidity is " + str(humidity) + "%"
        return text
    else:
        print(data['cod'])
        text = "Its windy, temperature is 28 degree celsius and humidity is 26%"
        return text
