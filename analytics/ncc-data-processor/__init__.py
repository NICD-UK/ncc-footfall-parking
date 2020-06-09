import json
import datetime
import logging
import urllib.request
from urllib.error import HTTPError


import azure.functions as func

CARPARKS_NAMES = ['Car park at Eldon Garden']
CARPARKS_API_URL = 'https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/entity?metric="Occupied%20spaces"&page=3' # page 3 has Eldon Garden
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
        carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)

        # join into a single output


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
    return(result)

def extract_carpark_data(response, carparks):
    tmp = json.loads(response)
    out = []
    for item in tmp['items']:
        if item['name'] in carparks:
            carpark_out = dict()
            carpark_out['name'] = item['name']
            carpark_out['timestamp'] = item['feed'][0]['timeseries'][0]['latest']['time']
            carpark_out['capacity'] = item['feed'][0]['meta']['totalSpaces']
            carpark_out['occupancy'] = item['feed'][0]['timeseries'][0]['latest']['value'] # ToDo double check this is the occupancy
            out.append(carpark_out)
    return(out)

def get_carpark_data(carparks, api_url):
    try:
        contents = urllib.request.urlopen(api_url).read() # not ideal !pagination!
    except HTTPError as e:
        logging.error("UO API call failed: " + e)
    out = extract_carpark_data(contents, carparks)
    return(out)    

# print(get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL))
# print(get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL))