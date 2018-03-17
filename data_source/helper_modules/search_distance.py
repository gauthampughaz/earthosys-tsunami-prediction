import sys
import os
import pandas as pd
import numpy as np


def find_latitude(dataset, lat):
	latitudes = dataset[:, 1]
	A = np.sort(latitudes)
	idx = A.searchsorted(lat)
	idx = np.clip(idx, 1, len(A)-1)
	left = A[idx-1]
	right = A[idx]
	idx -= lat - left < right - lat
	return A[idx]


def find_longitude(dataset, lng):
	longitudes = dataset[:, 0]
	A = np.sort(longitudes)
	idx = A.searchsorted(lng)
	idx = np.clip(idx, 1, len(A)-1)
	left = A[idx-1]
	right = A[idx]
	idx -= lng - left < right - lng
	return A[idx]


def find_distance(lat, lng, reg):
	dataset = get_dataset(lat, reg)
	lat = find_latitude(dataset, lat)
	dataset = dataset[dataset[:, 1] == lat]
	lng = find_longitude(dataset, lng)
	return dataset[dataset[:, 0] == lng][0][2]


def get_dataset(lat, reg):
	if int(reg) == 1:
		df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + "/../land_latitudes/{}.csv".format(int(lat)), sep='\t')
	elif int(reg) == 0:
		df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + "/../sea_latitudes/{}.csv".format(int(lat)), sep='\t')
	return df.as_matrix()

def get_nearest_lat_lng(lat, lng, reg):
	dataset = get_dataset(lat, reg)
	lat = find_latitude(dataset, lat)
	dataset = dataset[dataset[:, 1] == lat]
	lng = find_longitude(dataset, lng)
	return [lat, lng]
