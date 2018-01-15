import sys
import pandas as pd
sys.path.append('/home/gautham/earthosys/data_source/helper_modules/')
from search_distance import find_distance


def generate_distance(df = None, lat = None, lng = None, region = None):
	if df is not None:
		df['DISTANCE'] = pd.Series([0] * len(df.index), dtype=object)
		for i in range(len(df.index)):
			lat, lng = df['LATITUDE'][i], df['LONGITUDE'][i]
			if region == 1:
				df['DISTANCE'][i] = find_distance(float(lat), float(lng), df['REGION'][i])
			else:
				df['DISTANCE'][i] = 0
		return df
	else:
		if region == 1:
			return find_distance(float(lat), float(lng), region)
		else:
			return 0















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
