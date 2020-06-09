import json
import datetime
import logging
import urllib.request
from urllib.error import HTTPError


import azure.functions as func

FOOTFALL_SENSOR_NAMES = ['PER_PEOPLE_NC_B6324B1', 'PER_PEOPLE_NORTHUMERLAND_LINE_SHORT_DISTANCE_HEAD_6']
FOOTFALL_API_URL = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/{sensor_name}/json/"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('Next round of data collection!')
        
        # pull all street counter info
        footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)

        # pull the car parks data

        # persist to historical blob

        # overwrite latest


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

def extract_footfall(response):
    tmp = json.loads(response)
    out = dict()
    out['sensor_name'] = tmp['sensors'][0]['Sensor Name']
    out['measurement'] = -1 # where is actual measurement in the result?
    out['status'] = "quiet" # switch here for quiet/average/busy
    return(out)

def get_footfall_data(sensors, api_url):
    result = []
    for sensor in sensors:
        sensor_url = api_url.format(sensor_name = sensor)
        try:
            contents = urllib.request.urlopen(sensor_url).read()
            out = extract_footfall(contents)
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        result.append(out)
        print(out)
    return(result)

print(get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL))