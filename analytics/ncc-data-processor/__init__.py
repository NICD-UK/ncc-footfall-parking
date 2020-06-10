import json
import datetime
import logging
import random
import urllib.request
from urllib.error import HTTPError


import azure.functions as func

CARPARKS_NAMES = ['Car park at Eldon Garden']
CARPARKS_API_URL = 'https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/entity?metric="Occupied%20spaces"&page=3' # page 3 has Eldon Garden
FOOTFALL_SENSOR_NAMES = ['PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_0', 'PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_1']
FOOTFALL_API_URL = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/{sensor_name}/data/json/?starttime=202006102000&endtime=202006102100" # todo from time, until time
ACTIVITY_LEVELS = ['quiet', 'average', 'busy']

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

        # sanity check

        # persist to historical blob

        # overwrite latest


    logging.info('Python timer trigger function ran at %s', utc_timestamp)

def extract_footfall(sensor_name, response):
    tmp = json.loads(response)
    total_people_count = 0
    for record in tmp['sensors'][0]['data']['Walking North']:
        total_people_count += record['Value']
    for record in tmp['sensors'][0]['data']['Walking South']:
        total_people_count += record['Value']
    number_of_datapoints = len(tmp['sensors'][0]['data']['Walking North']) + len(tmp['sensors'][0]['data']['Walking South'])
    average_people_count = total_people_count / number_of_datapoints
    out = dict()
    out['sensor_name'] = sensor_name
    out['number_of_datapoints'] = number_of_datapoints 
    out['measurement'] = round(average_people_count, 1)
    return(out)

def get_footfall_data(sensors, api_url):
    result = []
    for sensor in sensors:
        sensor_url = api_url.format(sensor_name = sensor)
        try:
            contents = urllib.request.urlopen(sensor_url).read()
            out = extract_footfall(sensor, contents)
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        result.append(out)
    return(result)

def get_carpark_activity(current_occupancy):
    if current_occupancy < 50:
        return(ACTIVITY_LEVELS[0])
    elif current_occupancy < 75:
        return(ACTIVITY_LEVELS[1])
    return(ACTIVITY_LEVELS[2])

def extract_carpark_data(response, carparks):
    tmp = json.loads(response)
    out = []
    for item in tmp['items']:
        if item['name'] in carparks:
            carpark_out = dict()
            carpark_out['name'] = item['name']
            ts = item['feed'][0]['timeseries'][0]['latest']['time'] # get timestamp
            carpark_out['timestamp'] = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone().isoformat() # parse and format
            carpark_out['capacity'] = item['feed'][0]['meta']['totalSpaces']
            carpark_out['occupancy'] = item['feed'][0]['timeseries'][0]['latest']['value'] # ToDo double check this is the occupancy
            carpark_out['status'] = get_carpark_activity(carpark_out['occupancy'] * 100 / carpark_out['capacity'])  
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
    out['timestamp'] = str(datetime.datetime.now().astimezone().isoformat())
    out['response_time_ms'] = response_time.microseconds 
    out['footfall'] = footfall
    out['carparks'] = carparks
    return(out)

start_time = datetime.datetime.now()
footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)
carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)
out = format_output(footfall_out, carpark_out, datetime.datetime.now() - start_time)
print(json.dumps(out))