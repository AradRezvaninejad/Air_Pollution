from django.shortcuts import render
import requests
import urllib.parse
import time
import time
from datetime import datetime, timedelta
from .models import EducationCard, Article
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import json

API_KEY = "00afb1c16dc5d67dd05dfc0ad478a625"


def index(request):
    city = request.GET.get("city", "Tehran")

    city_encoded = urllib.parse.quote(city)

    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_encoded}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)
    print("Geo status:", geo_response.status_code)
    geo_data = geo_response.json()
    print("Geo data:", geo_data)

    if geo_response.status_code != 200 or not geo_data:
        return render(
            request,
            "main/index.html",
            {"error": f"City '{city}' not found or API error!", "city": city},
        )

    lat = geo_data[0].get("lat")
    lon = geo_data[0].get("lon")

    cards = EducationCard.objects.all()

    # گرفتن کیفیت هوا با Air Pollution API
    air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    air_response = requests.get(air_url)
    print("Air status:", air_response.status_code)
    air_data = air_response.json()
    print("Air data:", air_data)

    if (
        air_response.status_code != 200
        or "list" not in air_data
        or not air_data["list"]
    ):
        return render(
            request,
            "main/index.html",
            {"error": "Error fetching air pollution data.", "city": city},
        )

    air_info = air_data["list"][0]
    articles = Article.objects.all()[:6]
    ##########################################################################
    # df = pd.read_csv(
    #     r"C:\Users\rezva\OneDrive\Documents\GitHub\Air_Pollution\Air_Pollution\Air Pollution Index for Tehran, Mashhad, Ahvaz, and Isfahan From March to November 2024.CSV"
    # )
    # df["date_index"] = range(len(df))
    # cities = ['Tehran', 'Mashhad', 'Ahvaz', 'Isfahan']

    # predictions_dict = {}
    # mse_dict = {}

    # for city in cities:
    #     X = df[['date_index']]
    #     y = df[city]

    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #     # Random Forest
    #     rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    #     rf_model.fit(X_train, y_train)
    #     rf_pred = rf_model.predict(X_test)

    #     # Linear Regression
    #     lr_model = LinearRegression()
    #     lr_model.fit(X_train, y_train)
    #     lr_pred = lr_model.predict(X_test)

    #     # MSE
    #     mse_dict[city] = {
    #         "RandomForest": mean_squared_error(y_test, rf_pred),
    #         "LinearRegression": mean_squared_error(y_test, lr_pred)
    #     }

    #     # ذخیره داده‌ها برای Plotly
    #     predictions_dict[city] = {
    #         "dates": X_test['date_index'].tolist(),
    #         "y_test": y_test.tolist(),
    #         "RandomForest": rf_pred.tolist(),
    #         "LinearRegression": lr_pred.tolist()
    #     }

    # # تبدیل داده‌ها به JSON برای JS
    # predictions_json = json.dumps(predictions_dict)
    # mse_json = json.dumps(mse_dict)
    df = pd.read_csv(
        r"C:\Users\rezva\OneDrive\Documents\GitHub\Air_Pollution\Air_Pollution\Air Pollution Index for Tehran, Mashhad, Ahvaz, and Isfahan From March to November 2024.CSV"
    )
    df["date_index"] = range(len(df))
    cities = ['Tehran', 'Mashhad', 'Ahvaz', 'Isfahan']

    predictions_dict = {}
    mse_dict = {}

    for city in cities:
        X = df[['date_index']]
        y = df[city]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(X_test)

        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        lr_pred = lr_model.predict(X_test)

        # MSE
        mse_dict[city] = {
            "RandomForest": mean_squared_error(y_test, rf_pred),
            "LinearRegression": mean_squared_error(y_test, lr_pred)
        }

        # ذخیره داده‌ها برای Plotly
        predictions_dict[city] = {
            "dates": X_test['date_index'].tolist(),
            "y_test": y_test.tolist(),
            "RandomForest": rf_pred.tolist(),
            "LinearRegression": lr_pred.tolist()
        }

    # تبدیل داده‌ها به JSON برای JS
    predictions_json = json.dumps(predictions_dict)
    mse_json = json.dumps(mse_dict)


    return render(
        request,
        "main/index.html",
        {
            "city": city,
            "air_data": air_info,
            "cards": cards,
            "error": None,
            "articles": articles,
            "predictions_json": predictions_json,
            "mse_json": mse_json
        },
    )




# def air_history(request):
#     city = request.GET.get("city", "Tehran")

#     # Get city coordinates
#     geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(city)}&limit=1&appid={API_KEY}"
#     geo_data = requests.get(geo_url).json()
#     if not geo_data:
#         return render(
#             request, "main/air_history.html", {"error": "City not found!", "city": city}
#         )

#     lat = geo_data[0]["lat"]
#     lon = geo_data[0]["lon"]

#     # Get air pollution history (last 7 days)
#     end = int(time.time())
#     start = int((datetime.now() - timedelta(days=7)).timestamp())
#     air_url = f"https://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}"
#     air_data = requests.get(air_url).json()

#     if "list" not in air_data or not air_data["list"]:
#         return render(
#             request,
#             "main/air_history.html",
#             {"error": "No historical data found.", "city": city},
#         )

#     # Aggregate hourly data by day
#     daily_data = {}
#     for item in air_data["list"]:
#         day = datetime.fromtimestamp(item["dt"]).strftime("%b %d")
#         if day not in daily_data:
#             daily_data[day] = {"aqi": [], "pm2_5": [], "pm10": [], "no2": [], "o3": []}
#         daily_data[day]["aqi"].append(item["main"]["aqi"])
#         daily_data[day]["pm2_5"].append(item["components"]["pm2_5"])
#         daily_data[day]["pm10"].append(item["components"]["pm10"])
#         daily_data[day]["no2"].append(item["components"]["no2"])
#         daily_data[day]["o3"].append(item["components"]["o3"])

#     # Sort days and calculate daily average
#     sorted_days = sorted(daily_data.keys(), key=lambda d: datetime.strptime(d, "%b %d"))
#     dates, aqi_values, pm25_values, pm10_values, no2_values, o3_values = (
#         [],
#         [],
#         [],
#         [],
#         [],
#         [],
#     )

#     for day in sorted_days:
#         dates.append(day)
#         data = daily_data[day]
#         n = len(data["aqi"])
#         aqi_values.append(sum(data["aqi"]) / n)
#         pm25_values.append(sum(data["pm2_5"]) / n)
#         pm10_values.append(sum(data["pm10"]) / n)
#         no2_values.append(sum(data["no2"]) / n)
#         o3_values.append(sum(data["o3"]) / n)

#     context = {
#         "city": city,
#         "dates": dates,
#         "aqi_values": aqi_values,
#         "pm25_values": pm25_values,
#         "pm10_values": pm10_values,
#         "no2_values": no2_values,
#         "o3_values": o3_values,
#         "error": None,
#     }

#     return render(request, "main/air_history.html", context)


# def predict_view(request):
#     df = pd.read_csv(
#         "Air Pollution Index for Tehran, Mashhad, Ahvaz, and Isfahan From March to November 2024.CSV"
#     )
#     df["date (persian years)"] = range(len(df))
#     cities = ['Tehran', 'Mashhad', 'Ahvaz', 'Isfahan']
#     models = {}
#     predictions = {}
#     for city in cities:
#         X = df[['date (persian years)']]  
#         y = df[city]         
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#         model = RandomForestRegressor(n_estimators=100, random_state=42)
#         model.fit(X_train, y_train)
#         y_pred = model.predict(X_test)

#     mse = mean_squared_error(y_test, y_pred)
#     print(f"{city} - MSE: {mse:.2f}")

#     models[city] = model
#     predictions[city] = y_pred



    
