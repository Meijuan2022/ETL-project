from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import weather_download_data,weather_barchart,weather_data_etl
import os
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import requests,configparser
CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + '/config.ini')

API_KEY = config.get('DEV','API_KEY')

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def print_try():
    print("OK!")

geo_locations = {
    "uppsala": (59.9, 17.6),
    "ostersund": (63.2, 14.6),
    "lulea": (65.6, 22.1),
    "goteborg": (57.7, 12),
    "trelleborg": (55.4, 13.2),
    "stockholm": (59.3,18.0),
    "malmo" : (55.6,13.0),
}
def _request_weather_data():
    print("Ok")
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

def _save_to_database():
    sqlite_engine = create_engine("sqlite:///"+CURR_DIR_PATH+"/weather.db")
    weather_data = pd.read_csv(CURR_DIR_PATH + "/target/" +"weather_data.csv")

    weather_data.to_sql("weather_data",sqlite_engine,if_exists='append',index=False)

def _data_to_chart():
    CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    data = pd.read_json(CURR_DIR_PATH + "/data/json/weather.json")
    
    bar_width = 0.3
    x = np.arange(5)
    plt.bar(x-bar_width/2,data['temperature'],bar_width,label ='temperature')
    plt.bar(x+bar_width/2,data['humid'],bar_width,color = 'g', label = 'humid')
    plt.xticks(x,labels=data['city'])
    plt.legend()
    plt.title("Weather Bar Chart")
    plt.xlabel('City')
    plt.ylabel('weather_value ')
    plt.show()

with DAG("Download_Weather",
        default_args={
        "depends_on_past": False,
        "email": ["volta.xia@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5)},
        description="Weather Data from api.openweathermap.org",
           schedule=timedelta(days=1),
         start_date=datetime(2023, 5, 3),
         catchup=False,
         tags=["Weather Data"]) as dag:
    
    try_run = PythonOperator(
        task_id = "try_run",
        python_callable= print_try
    )
    
    request_weather_data = PythonOperator(
        task_id ="request_weather_data",
        python_callable = _request_weather_data
    )

    data_etl_tofiles = PythonOperator(
        task_id = "data_etl_tofiles",
        python_callable=weather_data_etl.transform_weather
    )

    save_to_database = PythonOperator(
        task_id = "save_to_database",
        python_callable=_save_to_database
    )
    barchart_data = PythonOperator(
        task_id = 'barchart_data',
        python_callable=_data_to_chart
    )
    try_run
    #request_weather_data  >> data_etl_tofiles >> save_to_database >> barchart_data
    