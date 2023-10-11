from flask import Flask, render_template_string, redirect, url_for
import folium
import requests

app = Flask(__name__)
OPEN_WEATHER_MAP_API_KEY = "1f9efcb0ec1a3aa943411f550790af73"

def fetch_weather_data(lat, lon):
    API_ENDPOINT = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=dewpoint_2m,precipitation,pressure_msl,cloudcover,visibility,windspeed_10m,winddirection_10m,temperature_80m,uv_index&current_weather=true&timeformat=unixtime&timezone=Europe%2FMoscow&forecast_days=1"
    response = requests.get(API_ENDPOINT)
    return response.json() if response.status_code == 200 else None

def generate_map(lat, lon, weather_data):
    m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
    
    folium.Marker(
        [lat, lon],
        tooltip=f"Cloud Coverage: {weather_data['hourly']['cloudcover'][0]}%",
    ).add_to(m)
    
    # Precipitation Tile Layer
    precipitation_tile_url = (f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={OPEN_WEATHER_MAP_API_KEY}")
    precipitation = folium.TileLayer(precipitation_tile_url, attr="OpenWeatherMap", name="Precipitation", overlay=True).add_to(m)
    
    # Cloud Coverage Tile Layer
    cloud_tile_url = (f"https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={OPEN_WEATHER_MAP_API_KEY}")
    clouds = folium.TileLayer(cloud_tile_url, attr="OpenWeatherMap", name="Cloud Coverage", overlay=True).add_to(m)
    
    # Wind Tile Layer
    wind_tile_url = (f"https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={OPEN_WEATHER_MAP_API_KEY}")
    wind = folium.TileLayer(wind_tile_url, attr="OpenWeatherMap", name="Wind", overlay=True).add_to(m)
    
    # Layer Control
    folium.LayerControl().add_to(m)
    
    return m._repr_html_()

@app.route('/')
def index():
    return render_template_string("""
    <html><body>
            <script>
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        window.location = "/weather/" + position.coords.latitude + "/" + position.coords.longitude;
                    });
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            </script>
        </body></html>""")

@app.route('/weather/<lat>/<lon>')
def weather(lat=None, lon=None):
    if not lat or not lon:
        return redirect(url_for('index'))

    weather_data = fetch_weather_data(lat, lon)
    map_html = generate_map(float(lat), float(lon), weather_data)
    hourly_data = weather_data['hourly']
    forecast = [
        {
            "hour": i + 1,
            "temperature": hourly_data['temperature_80m'][i],
            "dew_point": hourly_data['dewpoint_2m'][i],
            "wind_speed": hourly_data['windspeed_10m'][i]
        }
        for i in range(8)
    ]

    return render_template_string("""
    <html>
        <head>
            <title>Project Meteor</title>
                <style>
                    body, div, p {
                        margin: 0;
                        padding: 0;
                    }

                    body {
                        font-family: 'Verdana';
                        background-color: #f4f4f4;
                    }

                    #map {
                        position: fixed;
                        top: 0;
                        right: 0;
                        width: 50vw;
                        height: 28.125vw; /* 16:9 aspect ratio */
                        z-index: 1;
                        overflow: hidden;
                        padding: 20px;
                    }

                    .container {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-top: 20px;
                        margin-left: 20px;
                        flex-wrap: wrap;
                        gap: 115px;
                        width: calc(50% - 100px); /* Deducting for the gap between forecasts */
                        position: absolute;
                        left: 0;
                    }

                    .forecast-column {
                        flex: 1 1 calc(20% - 100px); /* Considering 100px as gap between columns */
                        box-sizing: border-box;
                        padding: 20px;
                        border: 1px solid #e5e5e5;
                        text-align: center;
                        background-color: #ffffff;
                        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                        transition: transform 0.3s, box-shadow 0.3s;
                    }

                </style>
            </head>
        <body>
            <div id="map">
                {{ map_html | safe }}
            </div>
            <div class="container">
                {% for item in forecast %}
                    <div class="forecast-column">
                        <h2>Hour {{ item.hour }}</h2>
                        <p>Temperature: {{ item.temperature }}°C</p>
                        <p>Dew Point: {{ item.dew_point }}°C</p>
                        <p>Wind Speed: {{ item.wind_speed }} m/s</p>
                    </div>
                {% endfor %}
            </div>
        </body>
    </html>
    """, map_html=map_html, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)
