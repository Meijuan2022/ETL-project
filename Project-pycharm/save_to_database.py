import os
import pandas as pd
from sqlalchemy import create_engine

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def sql_save():
    sqlite_engine = create_engine("sqlite:///"+CURR_DIR_PATH+"/weather.db")
    weather_data = pd.read_csv(CURR_DIR_PATH + "/target/" +"weather_data.csv")

    weather_data.to_sql("weather_data",sqlite_engine,if_exists='replace',index=False)