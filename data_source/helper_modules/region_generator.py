import sys
import pandas as pd
import requests


def generate_region(input_file):
	df = pd.read_csv('../{}'.format(input_file))
	df.insert(len(df.columns)-1, 'Region', 0)
	for i in range(len(df)):
	    lat, lng = df['Latitude'][i], df['Longitude'][i]
		url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio'.format(str(lat), str(lng))
	    api_result = requests.get(url).json()
	    ele_value = float(api_result["results"][0]["elevation"])
	    df['Region'][i] = 1 if ele_value >= 0 else 0
	df.to_csv('../{}'.format(input_file))


input_file = sys.argv[1]
generate_region(input_file)
