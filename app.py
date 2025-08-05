from flask import Flask, render_template, request
import requests
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEATHER_API_KEY = '9eaeef6c3edb3d8913e46ac936dd3d2d'
NEWS_API_KEY = '7d9217b300874c82b65259f84d41b63b'

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    logger.info("Request received for city  : %s", data.get("cod"))
    if str(data.get("cod")) != "200":
        return {"error": "City not found"}

    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }

    return weather

def get_news(city):
    url = f"https://newsapi.org/v2/everything?q={city}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    return [{"title": a["title"], "url": a["url"]} for a in articles]

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = {}
    if request.method == "POST":
        city = request.form.get("city")
        weather = get_weather(city)
        if "error" not in weather:
            news = get_news(city)
            weather["news"] = news
        weather_data = weather
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)