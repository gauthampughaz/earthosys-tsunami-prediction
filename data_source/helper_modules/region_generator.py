import sys
import pandas as pd
import requests


def generate_region(df = None, lat = None, lng = None):
	if df is not None:
		df.insert(len(df.columns), 'REGION', 0)
		for i in range(len(df)):
			lat, lng = df['LATITUDE'][i], df['LONGITUDE'][i]
			ele_value = get_elevation(lat=lat, lng=lng)
			df['REGION'][i] = 1 if ele_value >= 0 else 0
		return df
	else:
		ele_value = get_elevation(lat=lat, lng=lng)
		return 1 if ele_value >= 0 else 0


def get_elevation(lat, lng):
	url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio'.format(str(lat), str(lng))
	api_result = requests.get(url).json()
	return float(api_result["results"][0]["elevation"])
