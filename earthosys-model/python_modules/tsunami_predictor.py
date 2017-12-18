"""
Created on Fri Dec 8 14:24:47 2017

@author: gautham

	This is a machine learning model to predict the occurence of a tsunami with the help of the important
	characteristics of earthquakes as per International Tsunami Warning Center. The important characteristics
	of eathquakes specified for the occurence of tsunami by International Tsunami Warning Centerin the article
	" International Tsunami Warning Center. About Tsunamis. (2013). Accessed 14 January 2013. " are large,
	shallow earthquakes with an epicentre or fault line near or on the ocean floor. These are the main causes
	of a tsunami created by an earthquake.

	The above characteristics correspond to the following paremeters:
	1. Magitude
	2. Focal Depth
	3. Region of Occurrence such as Land(near ocean floor) or Ocean bed
	4. Distance from the ocean bed if the epicenter is in land.

Accuracy achieved so far with different Classification Algorithms:

Logistic Regression : 98.64
Naive Bayes : 98.37
Support Vector Machine with Linear Kernel : 98.1

"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
#from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
#from sklearn import tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
#from pandas.plotting import scatter_matrix


file_name = './model.pkl'


def features_relationship(df, array):
	colors = np.where(df.iloc[:, -1] > 0, 'b', 'r')
	legends = ['magnitude', 'depth', 'region', 'distance']
	f, ax_arr = plt.subplots(4,3)
	f.canvas.set_window_title('Feature Relationship')
	f.subplots_adjust(hspace=0.36, top=1.0, bottom=0.06, wspace=0.22, left=0.05, right=0.95)
	x, y = 0, 0
	for i in range(len(legends)):
		y = 0
		for j in range(len(legends)):
			if legends[i] != legends[j]:
				ax_arr[x, y].set(xlabel=legends[i], ylabel=legends[j])
				ax_arr[x, y].scatter(df.iloc[:, i], df.iloc[:, j], c=colors)
				y += 1
		x += 1
	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()
	plt.show()


def target_feature_split(dataset):
	return dataset[:, 0:4], dataset[:, -1]


def split_dataset(X, y):
	return train_test_split(X, y, test_size=0.30, random_state=28)


def train_model(features, labels):
	clf = LinearSVC(random_state=28)
	clf.fit(features, labels)
	_ = joblib.dump(clf, file_name)


def test_model(features):
	try:
		clf = joblib.load(file_name)
		return clf.predict(features)
	except:
		print('Please train the model...')

def find_score(pred_values, actual_values):
	return accuracy_score(pred_values, actual_values)


def predict_tsunami(features):
	try:
		clf = joblib.load(file_name)
		pred = clf.predict(features)
		return True if pred[0] else False
	except:
		print('Please train the model...')


labels =  ['magnitude', 'focal_depth', 'region', 'distance', 'class']
df = pd.read_csv('../dataset/dataset_final_v5.csv', names=labels)
dataset = df.as_matrix()

# View relationship between featuers
#features_relationship(df, dataset)

# Split dataset
X, y = target_feature_split(dataset)
features_train, features_test, labels_train, labels_test = split_dataset(X, y)

# Training the model
train_model(features_train, labels_train)

# Testing the model
pred = test_model(features_test)

# Evaluating the model
score = find_score(pred, labels_test)
print('Score : {}'.format(round(score * 100, 2)))

# Predicting new data
print('Tsunami : {}'.format(predict_tsunami([[9.3, 15, 1, -228]])))
