from glob import glob
import os
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
data_dir = CURR_DIR_PATH + "/data/"
target_dir = CURR_DIR_PATH + "/target/"


def load_dfs_from(glob_path):
    subject_data = []
    file_paths = glob(glob_path) 

    for path in file_paths:
        df = pd.read_csv(path)
        subject_data.append(df) 
    
    return subject_data, file_paths 

def transform_weather():
    data, paths = load_dfs_from(f"{data_dir}*.csv")
    weather_data = []

    for path, entry in zip(paths, data):
        entry = entry.to_dict("records")[0]
        weather_entry = {
                "date" : entry['date'],
                "city": os.path.basename(path)[:-4],
                "temperature": entry["main.temp"] - 273,
                "visibility":entry["visibility"],
                "clouds" : entry["clouds.all"],
                "pressure" : entry["main.pressure"],
                "humid": entry["main.humidity"]
        }
        weather_data.append(weather_entry)

    df = pd.DataFrame(weather_data, columns=['date',"city", "temperature", "visibility", "clouds", "pressure", "humid"])
    df.to_csv(target_dir + "weather_data.csv", index=False)#mode='a'
    df.to_json(CURR_DIR_PATH + "/data/json/weather.json")
 #   df.to_sql('weather_data',sqlite_engine,if_exists='replace',index=False)


    