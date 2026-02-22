import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry


# Process daily data. The order of variables needs to be the same as requested.

print("\nDaily data\n", daily_dataframe)

def get_weather(latitude, longitude):
# Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 50.904,
        "longitude": -1.4043,
        "daily": ["sunrise", "sunset"],
        "hourly": ["temperature_2m", "precipitation"],
        "models": "ukmo_seamless",
        "timezone": "Europe/London",
    }

    try: 
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
    #daily data
        daily = response.Daily()
        daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()
        daily_sunset = daily.Variables(1).ValuesInt64AsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        daily_data["sunrise"] = daily_sunrise
        daily_data["sunset"] = daily_sunset
        daily_dataframe = pd.DataFrame(data = daily_data)

    #filtering
        timezone = params["timezone"]
        today = pd.to_datetime('now', utc=True).tz_convert(timezone).date()
        daily_dataframe['data'] = daily_dataframe['date'].dt.tz_convert(timezone)
        today_df = daily_dataframe[daily_dataframe['date'].dt.date == today]

        if not today_df.empty:
            sunrise_time = pd.to_datetime(today_df.iloc[0]['sunrise'], unit = 's').strftime('%H:%M')
            sunset_time = pd.to_datetime(today_df.iloc[0]['sunset'], unit = 's').strftime('%H:%M')
            daily_summary = f"Sunrise: {sunrise_time} | Sunset: {sunset_time}"
        else:
            daily_summary = "Sun/Sunset data unavailable."
        
    #hourly data
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_dataframe = pd.DataFrame(data = hourly_data)

    #filtering
        timezone = params["timezone"]
        now = pd.to_datetime('now', utc=True).tz_convert(timezone) #get current time in zone
        start_time = now.floor('H') #forecast start time
        end_time = start_time + pd.Timedelta(hours=3) #forecast end time
        hourly_dataframe['date'] = hourly_dataframe['date'].dt.tz_convert(timezone)
        forecast_df = hourly_dataframe[(hourly_dataframe['date'] >= start_time) & (hourly_dataframe['date'] <= end_time)]. copy()

        hourly_summary = []
        if forecast_df.empty:
            hourly_summary.append("Hourly forecast unavailable.")
        else:
            for index,row in forecast_df.iterrows():
                time_str = row['date'].strftime('%H:%M')
                temp_str = f"{row['temperature']:.1f}0C"
                precip_str = f"{row['preciption']:.1f}mm"
                summary_line = f"{time_str} | {temp_str} | Rain: {precip_str}"
                hourly_summary.append(summary_line)

    #return both daily & hourly summaries
        return{
            "daily" : daily_summary
            "hourly" : hourly_summary 
        }

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return{
            "daily" : "Error fetching daily data."
            "hourly" : ["Error fetching hourly data."]
        }





