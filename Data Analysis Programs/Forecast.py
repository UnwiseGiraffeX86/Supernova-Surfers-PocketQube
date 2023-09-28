import tkinter as tk
import requests
import folium
from tkinterhtml import HtmlFrame

LATITUDE = '44.467035'
LONGITUDE = '26.106539'
CITY_RADIUS = 10
BASE_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=dewpoint_2m,precipitation_probability,pressure_msl,cloudcover,windspeed_80m,winddirection_10m,temperature_80m&current_weather=true&timeformat=unixtime&timezone=auto&forecast_days=1&models=best_match"

def fetch_weather_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def update_weather():
    weather_data = fetch_weather_data()
    if weather_data:
        temperature = weather_data['hourly']['temperature_80m'][0]
        dewpoint = weather_data['hourly']['dewpoint_2m'][0]
        precip_prob = weather_data['hourly']['precipitation_probability'][0]
        pressure = weather_data['hourly']['pressure_msl'][0]
        cloud_coverage = weather_data['hourly']['cloudcover'][0]
        wind_speed = weather_data['hourly']['windspeed_80m'][0]
        wind_direction = weather_data['hourly']['winddirection_10m'][0]

        temp_label.config(text=f"Temperature (80m): {temperature}°C")
        dewpoint_label.config(text=f"Dewpoint: {dewpoint}°C")
        precip_prob_label.config(text=f"Precipitation Probability: {precip_prob}%")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        cloud_cover_label.config(text=f"Cloud Coverage: {cloud_coverage}%")
        wind_speed_label.config(text=f"Wind Speed (80m): {wind_speed} m/s")
        wind_direction_label.config(text=f"Wind Direction: {wind_direction}°")

        return cloud_coverage
    return None

def create_map(cloud_coverage):
    m = folium.Map(location=[float(LATITUDE), float(LONGITUDE)], zoom_start=12)
    folium.Circle(
        location=[float(LATITUDE), float(LONGITUDE)],
        radius=CITY_RADIUS * 1000,
        popup=f"Cloud Coverage: {cloud_coverage}%",
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=cloud_coverage/100
    ).add_to(m)

    map_file = "map.html"
    m.save(map_file)
    return map_file

def display_map():
    cloud_coverage = update_weather()
    if cloud_coverage is not None:
        map_file = create_map(cloud_coverage)
        with open(map_file, 'r') as f:
            html_content = f.read()
            frame.set_content(html_content)

app = tk.Tk()
app.title('Weather Info using Open-Meteo API')

temp_label = tk.Label(app, font=("Arial", 14))
temp_label.pack(pady=5)

dewpoint_label = tk.Label(app, font=("Arial", 14))
dewpoint_label.pack(pady=5)

precip_prob_label = tk.Label(app, font=("Arial", 14))
precip_prob_label.pack(pady=5)

pressure_label = tk.Label(app, font=("Arial", 14))
pressure_label.pack(pady=5)

cloud_cover_label = tk.Label(app, font=("Arial", 14))
cloud_cover_label.pack(pady=5)

wind_speed_label = tk.Label(app, font=("Arial", 14))
wind_speed_label.pack(pady=5)

wind_direction_label = tk.Label(app, font=("Arial", 14))
wind_direction_label.pack(pady=5)

update_button = tk.Button(app, text="Update Weather", command=update_weather, font=("Arial", 12))
update_button.pack(pady=20)

frame = HtmlFrame(app, horizontal_scrollbar="auto")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

open_map_btn = tk.Button(app, text="Open Map", command=display_map)
open_map_btn.pack(pady=20)

update_weather()  # Fetch weather data on start

app.mainloop()
