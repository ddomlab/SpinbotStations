"""
This library is used for sending commands to the raspberry pi that drives all
the spinbot stations
"""

import requests, os
from datetime import datetime

class imagestation:
    """This class is used to automate the sending of HTTP request to the spinbot
    server to run subprocess
    """
    def __init__(self, pi_url: str, api_key: str):
        self.API_KEY = api_key
        self.PI_URL = f"{pi_url}/image-station"

    def ping(self):
        """Used to ping the image station camera

        Returns:
            int: status code returned by the server
        """
        return self._send('ping').status_code

    def capture(self, filename=''):
        r = self._send('capture')
        if not filename:
            filename = f"capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg"
        else:
            if not filename.endswith('.jpg'):
                filename = f"{filename}.jpg"
        os.makedirs(name='captures/', exist_ok=True)
        with open(f'captures/{filename}', 'wb') as f:
            f.write(r.content)
        return str(f"captures/{filename}")

    def _send(self, info: str):
        def_header = {
            "X-API-Key": self.API_KEY,
            "instruction": info
            }
        print(f"Sending {info} to {self.PI_URL}")
        return requests.get(
            self.PI_URL,
            headers=def_header,
            timeout=3
            )

#TODO pass in substrate number
#TODO live cam feed