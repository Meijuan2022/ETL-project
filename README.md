# Weather-Data- ETL
###Group-member: Meijuan Xia

weather_data ETL  with airflow(not succeed)
--download weather data with different city from API and save them to json files and csv files, database


# Tools
- airflow
- SQLAlchemy(sqlite)
- 
# IDE
- Pycharm, Visual Studio Code


## Run Codes
- Pycharm run __init__.py eller
- Visual Studio Code run download_weather.py 
- airflow webserver: localhost:8080
  ---name: airflow  password:airflow

## Problems which still need to be solved.
--I tried to run with airflow but failed, the first task keeps always running.I didn't know the reason. If I had more time I would try to solve the problem.
--I used the openweatherdata API,I registered and got API_KEY, but only kan download one group data at a time for free. I could not get the history data.
-- I would like figure out more different graphics if I would have more time.

# ETL-project
