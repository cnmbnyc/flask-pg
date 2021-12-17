from flask import Flask
import asyncio

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
