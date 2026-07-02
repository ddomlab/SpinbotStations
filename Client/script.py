import os
from dotenv import load_dotenv
from SpinbotStations import imagestation
from elnclient import ElnClient

load_dotenv()
eln_key = os.environ.get("ELN_KEY")
http_key = os.environ.get("HTTP_KEY")
if eln_key == None or http_key == None:
    raise ValueError("Missing eln and/or http key")

img_station = imagestation(
    pi_url='http://100.107.255.14:8080',
    api_key=http_key 
    )

# img_station.capture(filename='substrate_cap')

experiment = ElnClient(
    url="https://eln.ddomlab.org/api/v2",
    api_key=eln_key,
    title="Spinbot capture test",
    desc="This is a test of the API I am working with"
    )

experiment.upload_file(
    file_path=img_station.capture(filename='substrate_cap'), 
    comment="Capture of substrate"
    )