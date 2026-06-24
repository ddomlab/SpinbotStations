"""
Simple flask server

Routes:
    /           -> Public landing page
    /protected  -> Requires API key
"""

from flask import Flask
from auth import require_api_key

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to landing page!"

@app.route("/protected")
@require_api_key
def protected():
    return "You made it!!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)