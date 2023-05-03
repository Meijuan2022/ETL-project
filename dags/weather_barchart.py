import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# reading the database
data = pd.read_json(CURR_DIR_PATH + "/data/json/weather.json")

def charbar_show():

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