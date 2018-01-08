import sys
import pandas as pd
from search_distance import find_distance


def generate_distance(input_file = None, lat = None, lng = None, region = None):
	if input_file is not None:
		df = pd.read_csv('./{}'.format(input_file))
		df['DISTANCE'] = pd.Series([0] * len(df.index), dtype=object)
		for i in range(len(df.index)):
			lat, lng = df['LATITUDE'][i], df['LONGITUDE'][i]
			distance = find_distance(float(lat), float(lng), df['REGION'][i])
			df['DISTANCE'][i] = distance
		df.to_csv('./{}'.format(input_file))
	else:
		return find_distance(float(lat), float(lng), region)


input_file = sys.argv[1]
generate_distance(input_file=input_file)















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
