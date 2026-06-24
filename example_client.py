import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")
SERVER_ADDR = 'http://100.107.255.14:5000'     # This is the tailscale IP of raspi

if API_KEY is None:
    raise RuntimeError("Provide API key")

headers = {"X-API-Key": API_KEY}
r = requests.get(f"{SERVER_ADDR}/protected", headers=headers)
print(r.text)