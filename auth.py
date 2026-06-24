"""
Handles API key auth

To call a protected route, a client must send:
X-API-Key: <key>
"""

import os
from functools import wraps
from flask import request, abort
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY is not set. Please set before continuing")

def require_api_key(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        sent_key = request.headers.get("X-API-Key")
        print(request.headers)

        if sent_key is None:
            abort(401, description="Missing X-API-Key header")

        if sent_key != API_KEY:
            abort(401, description="Invalid API key")
        
        return route_function(*args, **kwargs)
    return wrapper