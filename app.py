from db import create_app
from routes import disaster_bp, weather_bp
from flask import render_template
import os

app = create_app()
app.register_blueprint(disaster_bp, url_prefix="/")
app.register_blueprint(weather_bp)

# @app.route("/")
# def home():
#     return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
