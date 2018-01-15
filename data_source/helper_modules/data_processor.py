import sys
import pandas as pd
sys.path.append('/home/gautham/earthosys/data_source/helper_modules/')
from region_generator import generate_region
from distance_generator import generate_distance


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
