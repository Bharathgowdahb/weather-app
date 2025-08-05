from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = '9eaeef6c3edb3d8913e46ac936dd3d2d'

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            weather = {
                "city": city.title(),
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
            }
        else:
            weather = {"error": "City not found"}

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)