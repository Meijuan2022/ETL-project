import requests,os,configparser
import pandas as pd
from datetime import datetime


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + '/config.ini')

API_KEY = config.get('DEV','API_KEY')

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


geo_locations = {
    "uppsala": (59.9, 17.6),
    "östersund": (63.2, 14.6),
    "luleå": (65.6, 22.1),
    "göteborg": (57.7, 12),
    "trelleborg": (55.4, 13.2)
}
def request_weather_data():
    
    for city in geo_locations:
        (lat, lon) = geo_locations[city]

        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }

        r = requests.get(WEATHER_URL, params=params)
        
        print("url:", r.url)
        print("http code:", r.status_code) 

        if r.status_code == 200: 
            json_data = r.json() 

            weather_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "weather": json_data["weather"][0], 
                "main": json_data["main"],
                "visibility": json_data["visibility"],
                "wind": json_data["wind"],
                "clouds": json_data["clouds"]
            }
            weather_data = pd.json_normalize(weather_data) 

            df = pd.DataFrame(weather_data)
            df.to_csv(CURR_DIR_PATH + "/data/" + city + ".csv", index=False)