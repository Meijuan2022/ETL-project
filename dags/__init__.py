import weather_download_data,weather_data_etl,save_to_database,weather_barchart



if __name__ == "__main__":
    weather_download_data.request_weather_data()
    weather_data_etl.transform_weather()
    save_to_database.sql_save()
    weather_barchart.charbar_show()

