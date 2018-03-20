import sys
import os
import pandas as pd
import math
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from region_generator import generate_region
from region_generator import get_elevation
from distance_generator import generate_distance
from distance_generator import find_distance
from search_distance import get_nearest_lat_lng
from ubidots import ApiClient

AUTH_TOKEN = "A1E-Jzxt1BSuMNBTwfRcKt0swcS5pJY2FP"
BASE_URL = "http://things.ubidots.com/api/v1.6/"
TSUNAMI_ID = "5aae46c0c03f972c1f33077b"

tsunami_alert = None

def process_data(input_file = None, input_data = None):
    if input_file is not None:
        df = pd.read_csv('./{}'.format(input_file))
        df = generate_region(df=df)
        df = generate_distance(df=df)
        df.drop('LATITUDE', axis=1, inplace=True)
        df.drop('LONGITUDE', axis=1, inplace=True)
        df.to_csv('./{}'.format(input_file))
    else:
        output_data = [input_data[0], input_data[1]]
        region = generate_region(lat=input_data[2], lng=input_data[3])
        output_data.append(region)
        output_data.append(generate_distance(lat=input_data[2], lng=input_data[3], region=region))
        return output_data


def get_additional_info(lat, lng):
    additional_info = {}
    region = generate_region(lat=lat, lng=lng)
    nearest_lat_lng = get_nearest_lat_lng(lat=lat, lng=lng, reg=region)
    additional_info["nearest_lat"] = nearest_lat_lng[0]
    additional_info["nearest_lng"] = nearest_lat_lng[1]
    additional_info["distance"] = round(abs(find_distance(lat=lat, lng=lng, reg=region)), 2)
    additional_info["location"] = get_location(lat=additional_info["nearest_lat"], lng=additional_info["nearest_lng"])
    elevation = get_elevation(lat=lat, lng=lng)
    if elevation < 0:
        additional_info["speed"] = str(round(math.sqrt(9.81 * abs(elevation)) * 3.6, 2))
    else:
        additional_info["speed"] = "NA"
    return additional_info

def get_location(lat, lng):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {"latlng": "{}, {}".format(float(lat), float(lng)), "sensor": "true", "key": "AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio"}
    api_result = requests.get(url, params=params).json()
    if api_result["results"] != []:
        return api_result["results"][0]["formatted_address"]
    else:
        return "Location unavailable."

def init():
    global tsunami_alert, AUTH_TOKEN, BASE_URL, TSUNAMI_ID
    api = ApiClient(token=AUTH_TOKEN, base_url=BASE_URL)
    tsunami_alert = api.get_variable(TSUNAMI_ID)


def alert_bot():
    init()
    global tsunami_alert
    try:
        _val = tsunami_alert.save_value({"value": 1})
        while _val == 0:
            _val = tsunami_alert.get_values(1)[0]["value"]
        print("Alerted")
    except Exception as e:
        print("Not alerted due to error {}".format(e))








# File handing method..

'''

import sys
import csv
import requests


input_file = sys.argv[1]
with open('../{}'.format(input_file), 'r') as in_f:
    with open('../{}'.format(input_file), 'w') as out_f:

        out = []

        reader = csv.reader(in_f)
        writer = csv.writer(out_f, lineterminator='\n')

        heading = next(reader)
        heading.append('REGION')
        heading.append('ELEVATION')
        out.append(heading)

        for row in reader:
            url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio'.format(str(row[2][:-2]), str(row[3][:-2]))
            api_result = requests.get(url).json()
            ele_value = float(api_result["results"][0]["elevation"])

            row.append(1 if ele_value >= 0 else 0)
            row.append(ele_value)
            out.append(row)

        writer.writerows(out)

'''
