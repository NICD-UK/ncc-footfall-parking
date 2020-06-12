import os
import json
import datetime
import logging
import random
import logging
import urllib.request
from azure.storage.blob import BlobServiceClient
from urllib.error import HTTPError

CARPARKS_NAMES = ['Eldon%20Square', 'Claremont%20Road', 'Dean%20Street', 'Eldon%20Garden', 'Ellison%20Place', 'Grainger%20Town', 'Manors']
CARPARKS_API_URL = 'https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/entity?metric="Occupied%20spaces"&name="{car_park}"'
FOOTFALL_SENSOR_NAMES = ['PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_0', 'PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_1']
FOOTFALL_API_URL = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/{sensor_name}/data/json/?starttime={start_time}&endtime={end_time}" 
FOOTFALL_TIME_WINDOW_MINUTES = 60 # RAISE at next meet-up
ACTIVITY_LEVELS = ['quiet', 'average', 'busy']

FILE_NAME_LATEST_CITY_STATE = "latest_city_state.json"
FILE_NAME_LATEST_CAR_PARKS = "latest_car_parks.json"
FILE_NAME_CREDENTIALS = "/home/ncc/ncc-footfall-parking/analytics/vm-script/settings.json" # todo uff

# logging
logging.basicConfig(format='%(asctime)s %(funcName)s [%(lineno)d] %(message)s', level=logging.INFO)

# start
logging.info('It is the beginning, is it not?')

# load credentials/settings
with open(FILE_NAME_CREDENTIALS, 'r') as fIn:
    creds = json.load(fIn)
logging.debug("Credentials loaded.")

def extract_footfall(sensor_name, response):
    logging.debug(f"{sensor_name};{response}")
    tmp = json.loads(response)
    out = dict()
    total_people_count = 0

    # check that UO returned some data
    if len(tmp['sensors'][0]['data']) > 0:
        for record in tmp['sensors'][0]['data']['Walking North']:
            total_people_count += record['Value']
        for record in tmp['sensors'][0]['data']['Walking South']:
            total_people_count += record['Value']
        number_of_datapoints = len(tmp['sensors'][0]['data']['Walking North']) + len(tmp['sensors'][0]['data']['Walking South'])
        average_people_count = total_people_count / number_of_datapoints
    else:
        # end early - no datapoints returned; don't return 0 as activity level
        return(out)
    
    out['sensor_name'] = sensor_name
    out['number_of_datapoints'] = number_of_datapoints 
    out['average_people_count'] = round(average_people_count, 1)
    return(out)

def get_footfall_data(sensors, api_url):
    logging.debug(f"{sensors};{api_url}")
    result = []
    for sensor in sensors:
        time_now = datetime.datetime.now()
        end_time = datetime.datetime.now().strftime("%Y%m%d%H%m")
        start_time = (time_now - datetime.timedelta(minutes=FOOTFALL_TIME_WINDOW_MINUTES)).strftime("%Y%m%d%H%m")
        sensor_url = api_url.format(sensor_name = sensor, start_time = start_time, end_time = end_time)
        try:
            contents = urllib.request.urlopen(sensor_url).read()
            out = extract_footfall(sensor, contents)
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        result.append(out)
    return(result)

def get_carpark_activity(current_occupancy): # todo recode for easier mod
    logging.debug(f"{current_occupancy}")
    if current_occupancy < 35:
        return(ACTIVITY_LEVELS[0])
    elif current_occupancy < 75:
        return(ACTIVITY_LEVELS[1])
    return(ACTIVITY_LEVELS[2])

def extract_carpark_data(response, carparks):
    logging.debug(f"{response};{carparks}")
    tmp = json.loads(response)
    carpark_out = dict()
    if len(tmp['items']) > 0:
        carpark_out['name'] = tmp['items'][0]['meta']['name']
        ts = tmp['items'][0]['feed'][0]['timeseries'][0]['latest']['time'] # get timestamp
        carpark_out['timestamp'] = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone().isoformat() # parse and format
        carpark_out['capacity'] = tmp['items'][0]['feed'][0]['meta']['totalSpaces']
        carpark_out['occupancy'] = tmp['items'][0]['feed'][0]['timeseries'][0]['latest']['value']
        carpark_out['reserved_bays'] = 0 # todo update once we know
        carpark_out['free_spaces'] = carpark_out['capacity'] - carpark_out['occupancy'] - carpark_out['reserved_bays']
        carpark_out['state'] = get_carpark_activity(carpark_out['occupancy'] * 100 / carpark_out['capacity'])  
    return(carpark_out)

def get_carpark_data(carparks, api_url):
    logging.debug(f"{carparks};{api_url}")
    out = []
    for carpark in carparks:
        tmp_url = api_url.format(car_park = carpark)
        logging.debug(tmp_url)
        try:
            contents = urllib.request.urlopen(tmp_url).read() 
        except HTTPError as e:
            logging.error("UO API call failed: " + e)
        out.append(extract_carpark_data(contents, carpark))
    return(out)    

def get_city_activity(footfall): # todo record for easier mod
    logging.debug(f"{footfall}")
    total_footfall = 0
    for record in footfall:
        # check if something fell over
        if 'average_people_count' in record:
            total_footfall += record['average_people_count']
        # else: log problem todo
    logging.info(f"total_footfall: {total_footfall}; footfall average: {footfall}")
    total_footfall = total_footfall / len(record)    
    if total_footfall < 25:
        return(ACTIVITY_LEVELS[0])
    elif total_footfall < 100:
        return(ACTIVITY_LEVELS[1])
    return(ACTIVITY_LEVELS[2])

def format_city_state(footfall, response_time):
    logging.debug(f"{footfall},{response_time}")
    out = dict()
    out['timestamp'] = str(datetime.datetime.now().astimezone().isoformat())
    out['response_time_us'] = response_time.microseconds 
    out['city_state'] = get_city_activity(footfall)
    out['footfall'] = footfall
    return(out)

def format_car_parks(carparks, response_time):
    logging.debug(f"{carparks},{response_time}")
    out = dict()
    out['timestamp'] = str(datetime.datetime.now().astimezone().isoformat())
    out['response_time_us'] = response_time.microseconds 
    out['carparks'] = carparks
    return(out)    

# ToDo - put everything into classes; tidy-up this mess
# CITY STATE
# start the clock
start_time = datetime.datetime.now()

# pull all footfall data
footfall_out = get_footfall_data(FOOTFALL_SENSOR_NAMES, FOOTFALL_API_URL)

# persist city state
file_name = f"ncc-city-state-{datetime.datetime.now().isoformat()}.json".replace(':','-')
local_file_name = "/home/ncc/ncc-footfall-parking/analytics/vm-script/out" + os.sep + file_name # todo uff

# local copy
city_state = format_city_state(footfall_out, datetime.datetime.now() - start_time)
with open(local_file_name, 'w') as fOut:
    fOut.write(json.dumps(city_state))

# blob storage client historical
blob_service_client = BlobServiceClient.from_connection_string(creds['SAS_BLOB_CONNECTION'])
blob_client = blob_service_client.get_blob_client(container=creds['CONTAINER_NAME'], blob=f"historical/citystate/{file_name}")

# upload to container
with open(local_file_name, "rb") as data:
    blob_client.upload_blob(data)

# only overwrite the latest file if there is at least one data sample
if len(footfall_out[0]) > 0:
    # overwrite latest city state
    blob_client = blob_service_client.get_blob_client(container=creds['CONTAINER_NAME'], blob=FILE_NAME_LATEST_CITY_STATE)

    # upload to container
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite = True)

    # additional one liner
    with open('/home/ncc/ncc-footfall-parking/analytics/vm-script/city_state_log.csv', 'a') as fOut:
        fOut.write(f"{city_state['timestamp']},{city_state['city_state']},{city_state['footfall'][0]['average_people_count']},,{city_state['footfall'][1]['average_people_count']},{city_state['response_time_us']}\n")

logging.info(footfall_out)

# CAR PARKS
# re-start the clock for car parks
start_time = datetime.datetime.now()

# pull the car parks data
carpark_out = get_carpark_data(CARPARKS_NAMES, CARPARKS_API_URL)
print(carpark_out)
# # persist car parks
file_name = f"ncc-car-parks-{datetime.datetime.now().isoformat()}.json".replace(':','-')
local_file_name = "/home/ncc/ncc-footfall-parking/analytics/vm-script/out" + os.sep + file_name # todo uff

# # local copy
with open(local_file_name, 'w') as fOut:
    fOut.write(json.dumps(format_car_parks(carpark_out, datetime.datetime.now() - start_time)))

# # blob storage client historical
blob_service_client = BlobServiceClient.from_connection_string(creds['SAS_BLOB_CONNECTION'])
blob_client = blob_service_client.get_blob_client(container=creds['CONTAINER_NAME'], blob=f"historical/carparks/{file_name}")

# # upload to container
with open(local_file_name, "rb") as data:
    blob_client.upload_blob(data)

# only overwrite the latest file if there is at least one data sample
if len(carpark_out[0]) > 0:
    # overwrite latest city state
    blob_client = blob_service_client.get_blob_client(container=creds['CONTAINER_NAME'], blob=FILE_NAME_LATEST_CAR_PARKS)

    # upload to container
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite = True)
logging.info(carpark_out)

logging.info("It is done.")    