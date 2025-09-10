from django.shortcuts import render
import requests

API_KEY = "121000eab15652ca1cb78077be2beec9"

def index(request):
    city = request.GET.get("city", "").strip()
    error = None
    air_data = None

    if city:  # فقط وقتی کاربر چیزی نوشت
        try:
            # گرفتن مختصات
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo_resp = requests.get(geo_url).json()

            if not geo_resp:
                error = f"City '{city}' not found!"
            else:
                lat = geo_resp[0]["lat"]
                lon = geo_resp[0]["lon"]

                # گرفتن داده آلودگی
                air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
                air_resp = requests.get(air_url).json()

                if "list" in air_resp and air_resp["list"]:
                    air_data = air_resp["list"][0]
                else:
                    error = "No air quality data found!"
        except Exception as e:
            error = str(e)

    return render(request, "main/index.html", {
        "city": city,
        "air_data": air_data,
        "error": error
    })