import sys
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
	if int(reg) == 1:
		df = pd.read_csv('/home/gautham/earthosys/data_source/land_latitudes/{}.csv'.format(int(lat)), sep='\t')
	elif int(reg) == 0:
		df = pd.read_csv('/home/gautham/earthosys/data_source/sea_latitudes/{}.csv'.format(int(lat)), sep='\t')
	dataset = df.as_matrix()
	lat = find_latitude(dataset, lat)
	dataset = dataset[dataset[:, 1] == lat]
	lng = find_longitude(dataset, lng)
	result = dataset[dataset[:, 0] == lng][0][2]
	return result
