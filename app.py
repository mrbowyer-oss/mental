from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ It works! Flask is alive on Render."

@app.route("/debug")
def debug():
    return "🛠 Debug route is working too."
