import requests
import json
import random

def fetch_weather(lat, lon, city):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 7,
    }
    print(f"\nFetching weather for: {city}")
    try:
        response = requests.get(url, params=params, timeout=10)
        # raises HTTPError for 4xx/5xx status codes
        response.raise_for_status()
        print(f"Status: {response.status_code} OK")
        # parse JSON response into a Python dict
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Connection error. Check internet.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None

def mock_data(city):
    # fallback when network is not available
    # same city always gives same mock values
    random.seed(hash(city) % 1000)
    base = {"Mumbai": 32, "London": 15, "New York": 22}.get(city, 25)
    dates = [f"2025-06-{d:02d}" for d in range(1, 8)]
    hours = [f"2025-06-01T{h:02d}:00" for h in range(24)]
    return {
        "daily": {
            "time": dates,
            "temperature_2m_max": [round(base + random.uniform(0, 5), 1) for _ in dates],
            "temperature_2m_min": [round(base - random.uniform(3, 8), 1) for _ in dates],
            "precipitation_sum":  [round(random.uniform(0, 15), 1) for _ in dates],
        },
        "hourly": {
            "time": hours,
            "temperature_2m": [round(base + random.uniform(-4, 6), 1) for _ in hours],
        }
    }

def show_forecast(data, city):
    daily = data["daily"]
    print(f"\n7-Day Forecast - {city}")
    print(f"{'Date':<12} {'Max':>6} {'Min':>6} {'Rain':>8}")
    print("-" * 36)
    for d, hi, lo, rain in zip(daily["time"], daily["temperature_2m_max"],
                                daily["temperature_2m_min"], daily["precipitation_sum"]):
        print(f"{d:<12} {hi:>6.1f} {lo:>6.1f} {rain:>8.1f}")

def filter_hot_hours(data, threshold=28.0):
    # return only hours where temperature exceeds the threshold
    hourly = data["hourly"]
    return [(t, temp) for t, temp in zip(hourly["time"], hourly["temperature_2m"])
            if temp and temp > threshold]

def save_json(data, filename):
    try:
        with open(filename, "w") as f:
            # indent=2 makes the file human-readable
            json.dump(data, f, indent=2)
        print(f"\nSaved to: {filename}")
    except IOError as e:
        print(f"Save failed: {e}")

def load_json(filename):
    try:
        with open(filename, "r") as f:
            # parse JSON file back into a Python dict
            data = json.load(f)
        print(f"Loaded keys: {list(data.keys())}")
        return data
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
    return None
if __name__ == "__main__":
    cities = [
        ("Mumbai",   19.076,  72.877),
        ("London",   51.507,  -0.127),
        ("New York", 40.712, -74.006),
    ]
    for city, lat, lon in cities:
        data = fetch_weather(lat, lon, city)
        if data is None:
            print(f"Using mock data for {city}")
            data = mock_data(city)
        show_forecast(data, city)
        hot = filter_hot_hours(data, threshold=28.0)
        if hot:
            print(f"\nHours above 28C in {city}:")
            for t, temp in hot[:5]:
                print(f"  {t}  {temp}C")
            if len(hot) > 5:
                print(f"  ...and {len(hot)-5} more")
        else:
            print(f"No hours above 28C in {city}")
        if city == "Mumbai":
            save_json(data, "mumbai_weather.json")
            load_json("mumbai_weather.json")

    # test error handling with a simulated 404 response
    print("\nTesting error handling with bad endpoint:")
    try:
        r = requests.models.Response()
        r.status_code = 404
        raise requests.exceptions.HTTPError("404 Not Found", response=r)
    except requests.exceptions.HTTPError as e:
        print(f"Caught: {e}")
