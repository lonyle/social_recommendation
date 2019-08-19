# regression on the recommendation probability given the reward and other factors

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import pandas as pd
import numpy as np
import csv
import json
import os
import matplotlib.pyplot as plt
from sklearn.externals import joblib

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

business_filename = 'data/business_checkin_review.json'
csv_filename = 'data/business_regression.csv'

def json2csv(business_filename, csv_filename):
	print ('constructing the csv file ' + csv_filename + ' from json file ' + business_filename)
	csv_file = open(csv_filename, 'w')
	writer = csv.writer(csv_file)
	columns = ['reward', 'stars', 'review_count', 'p_with', 'p_without', 'price_rating', 'effective_price', 'N_receivers']
	writer.writerow(columns)

	input_file = open(business_filename)
	line = input_file.readline()
	while line:
		data = json.loads(line)
		reward = 0
		if data['check_in_offer_text']:
			reward = 1 
		review_count = data['review_count'] # may change to other forms
		#price_range = data['attributes']['RestaurantsPriceRange2']
		if ('p_with' in data) and data['p_with'] and data['price_rating']:
			#if data['p_with'] != 0:
			#if review_count > 100:
			# !!! convert the price_rating to effective price [1,5]->[0,1]
			effective_price = (5-data['price_rating']) / 4
			writer.writerow([reward, data['stars'], review_count, data['p_with'],\
			 data['p_without'], data['price_rating'], effective_price, data['N_receivers']])

		line = input_file.readline()
	input_file.close()
	csv_file.close()
	print ('construction completed.')

def transform_tmp():
	df = pd.read_csv(csv_filename)
	reward_vec = df['reward']
	trans_reward_vec = []
	for reward in reward_vec:
		trans_reward_vec.append(0.1 * reward) # normalized 10%

	price_rating_vec = df['price_rating']
	effective_price_vec = []
	for price_rating in price_rating_vec:
		effective_price_vec.append( (5-price_rating)/4 )

	df['trans_reward'] = trans_reward_vec
	df['effective_price'] = effective_price_vec

	df.to_csv(csv_filename)


def preprocessing():
	if not os.path.isfile(csv_filename):
		json2csv(business_filename, csv_filename)
	df = pd.read_csv(csv_filename)
	reward_df = df.loc[df['reward'] == 1]
	#reward_df = reward_df.nlargest(100, 'review_count')
	quantile_1 = reward_df.review_count.quantile(0.45)
	quantile_2 = reward_df.review_count.quantile(0.55)
	reward_df = reward_df.loc[(reward_df['review_count'] > quantile_1) & (reward_df['review_count'] < quantile_2)]
	
	nonreward_df = df.loc[df['reward'] == 0]
	#nonreward_df = nonreward_df.nlargest(100, 'review_count')
	quantile_1 = nonreward_df.review_count.quantile(0.45)
	quantile_2 = nonreward_df.review_count.quantile(0.55)
	nonreward_df = nonreward_df.loc[(nonreward_df['review_count'] > quantile_1) & (nonreward_df['review_count'] < quantile_2)]
	# here, we use the original result without filtering
	filtered_df = df#pd.concat([reward_df, nonreward_df])

	features_name = ['trans_reward', 'effective_price']
	label_name = ['review_count']
	X = filtered_df.as_matrix(columns=features_name) # return a numpy array
	y = filtered_df.as_matrix(columns=label_name)
	sample_weight = filtered_df['N_receivers']

	return X, y, sample_weight

def linear_regression(X, y, sample_weight):
	# Create linear regression object
	regr = linear_model.LinearRegression()

	# Train the model using the training sets
	print ('>>> training the model')
	regr.fit(X, y) # do not use weight
	#regr.fit(X, y, sample_weight) # use weight

	print ('>>> evaluating the model')
	y_pred = regr.predict(X)
	# The coefficients
	print ('Coefficients: \n', regr.coef_)
	print ('Intercept:', regr.intercept_)

	print ('Parameters:', regr.get_params())

	# The mean squared error
	print("Mean squared error: %.2f"
	      % mean_squared_error(y, y_pred))

	print ('The score is:', regr.score(X, y))
	return regr

def linear_regression_price():
	regr_price = linear_model.LinearRegression()
	df = pd.read_csv(csv_filename)
	X = df.as_matrix(columns=['effective_price'])
	y = df.as_matrix(columns=['review_count'])
	regr_price.fit(X, y) 

	print ('>>> evaluating the model')
	y_pred = regr_price.predict(X)
	# The coefficients
	print ('Coefficients: \n', regr_price.coef_)
	print ('Intercept:', regr_price.intercept_)

	print ('Parameters:', regr_price.get_params())

	# The mean squared error
	print("Mean squared error: ", mean_squared_error(y, y_pred))

	print ('The score is:', regr_price.score(X, y))
	return regr_price

def logit_regression(X, y, sample_weight):
	# y = logit(theta * x)
	# x is the same
	# y_label = ln(y/(1-y))
	# TODO
	return model


if __name__ == '__main__':
	#transform_tmp()

	# X, y, sample_weight = preprocessing()
	# regr = linear_regression(X, y, sample_weight)

	linear_regression_price()

	#plt.scatter(X[:,1], y, color='blue')
	#plt.plot(X[:,0], regr.predict(X), color='k')
	#plt.show()
