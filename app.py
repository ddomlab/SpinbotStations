"""
Simple flask server

Routes:
    /               -> Public landing page
    /imagestation   -> Requires API key
            - "ping" - confirms server status
            - "capture" - returns jpeg img
"""

from flask import Flask, request, send_file, abort
from auth import require_api_key
from SpinbotStationsDrivers import imagestation
import io

app = Flask(__name__)
station = imagestation()

@app.route("/")
def index():
    return "Welcome to landing page!"

@app.route("/imagestation")
@require_api_key
def run():
    match request.headers['instruction']:
        case 'ping':
            pass
        case 'capture':
            try:
                image_bytes = station.capture()
            except RuntimeError as e:
                abort(500, description=str(e))
            
            return send_file(
                io.BytesIO(image_bytes),
                mimetype="image/jpeg",
                as_attachment=False,
                download_name="capture.jpg"
            )
        case _: # problem with instruction
            abort(400, description=f"Unknown instruction: {request.headers['instruction']!r}")
    
    return "Done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)