import sys
import pandas as pd
import requests


def generate_region(df = None, lat = None, lng = None):
	if df is not None:
		df.insert(len(df.columns), 'REGION', 0)
		for i in range(len(df)):
			lat, lng = df['LATITUDE'][i], df['LONGITUDE'][i]
			url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio'.format(str(lat), str(lng))
			api_result = requests.get(url).json()
			ele_value = float(api_result["results"][0]["elevation"])
			df['REGION'][i] = 1 if ele_value >= 0 else 0
		return df
	else:
		url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key=AIzaSyBv4lMhBkh4Sk8MjjMy9cmSC8XFX0v-Zio'.format(str(lat), str(lng))
		api_result = requests.get(url).json()
		ele_value = float(api_result["results"][0]["elevation"])
		return 1 if ele_value >= 0 else 0
