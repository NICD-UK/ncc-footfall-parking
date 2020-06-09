import json
import datetime
import logging
import random
import urllib.request
from urllib.error import HTTPError


import azure.functions as func

CARPARKS_NAMES = ['Car park at Eldon Garden']
CARPARKS_API_URL = 'https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/entity?metric="Occupied%20spaces"&page=3' # page 3 has Eldon Garden
FOOTFALL_SENSOR_NAMES = ['PER_PEOPLE_NC_B6324B1', 'PER_PEOPLE_NORTHUMERLAND_LINE_SHORT_DISTANCE_HEAD_6']
FOOTFALL_API_URL = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/{sensor_name}/json/"
BUSYNESS_LEVELS = ['quiet', 'average', 'busy']

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('Next round of data collection!')
        
        # start the clock
        start_time = datetime.datetime.now()

        # pull all footfall data
        footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)

        # pull the car parks data
        carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)

        # join into a single output
        out = format_output(footfall_out, carpark_out, datetime.datetime.now() - start_time)

        # persist to historical blob

        # overwrite latest


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

def extract_footfall(response):
    tmp = json.loads(response)
    out = dict()
    out['sensor_name'] = tmp['sensors'][0]['Sensor Name']
    out['measurement'] = -1 # where is actual measurement in the result?
    out['status'] = random.choice(BUSYNESS_LEVELS) # ToDo some clever switch
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

def get_carpark_business(current_occupancy):
    if current_occupancy < 35:
        return(BUSYNESS_LEVELS[0])
    elif current_occupancy < 70:
        return(BUSYNESS_LEVELS[1])
    return(BUSYNESS_LEVELS[2])

def extract_carpark_data(response, carparks):
    tmp = json.loads(response)
    out = []
    for item in tmp['items']:
        if item['name'] in carparks:
            carpark_out = dict()
            carpark_out['name'] = item['name']
            carpark_out['timestamp'] = item['feed'][0]['timeseries'][0]['latest']['time'] # ToDo parse timestamp
            carpark_out['capacity'] = item['feed'][0]['meta']['totalSpaces']
            carpark_out['occupancy'] = item['feed'][0]['timeseries'][0]['latest']['value'] # ToDo double check this is the occupancy
            carpark_out['status'] = get_carpark_business(carpark_out['occupancy'] / carpark_out['capacity']) 
            out.append(carpark_out)
    return(out)

def get_carpark_data(carparks, api_url):
    try:
        contents = urllib.request.urlopen(api_url).read() # not ideal !pagination!
    except HTTPError as e:
        logging.error("UO API call failed: " + e)
    out = extract_carpark_data(contents, carparks)
    return(out)    

def format_output(footfall, carparks, response_time):
    out = dict()
    out['timestamp'] = str(datetime.datetime.now())
    out['response_time_ms'] = response_time.microseconds 
    out['footfall'] = footfall
    out['carparks'] = carparks
    return(out)


start_time = datetime.datetime.now()
footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)
carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)
out = format_output(footfall_out, carpark_out, datetime.datetime.now() - start_time)
print(json.dumps(out))    