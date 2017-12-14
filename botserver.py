#!/usr/bin/python3

from flask import Flask
from flask import request
import json

from nplate import handle_update

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def hello():
    update = request.data.decode("utf8")
    update = json.loads(update)
    handle_update(update)
    
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0")
