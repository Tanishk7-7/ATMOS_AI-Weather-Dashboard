import requests
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_data(place,days):
    url =f'https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    filtered_data = data['list']
    curr = filtered_data[0]

    temp = curr["main"]["temp"]
    feels_like = curr["main"]["feels_like"]
    humidity = curr["main"]["humidity"]
    pressure = curr["main"]["pressure"]

    wind_speed = curr["wind"]["speed"]
    wind_deg = curr["wind"]["deg"]

    visibility = curr["visibility"]

    condition = curr["weather"][0]["main"]
    curr_desc = curr["weather"][0]["description"]
    icon = curr["weather"][0]["icon"]

    clouds = curr["clouds"]["all"]

    rain_prob = curr["pop"] * 100   
    current_weather = {
    "temp": temp,
    "feels_like": feels_like,
    "humidity": humidity,
    "pressure": pressure,
    "wind_speed": wind_speed,
    "visibility": visibility,
    "condition": condition, 
    "description": curr_desc,
    "icon": icon,
    "clouds": clouds,
    "rain_probability": rain_prob,
    }

    filtered_data = filtered_data[:8*days]

    return filtered_data , current_weather


if __name__ == '__main__':
    print(get_data(place='tokyo', days=1))
