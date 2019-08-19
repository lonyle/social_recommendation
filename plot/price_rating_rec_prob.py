csv_filename = 'data/business_regression.csv'

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

df = pd.read_csv(csv_filename)

def aggregate_by_key(key_vec, value_vec):
	idx = 0
	count_dict = {}
	sum_dict = {}
	for idx in range(len(key_vec)):
		key = int( (key_vec[idx])*1 ) / 1 + 0.5		
		#key = key_vec[idx]
		value = value_vec[idx]
		if key not in count_dict:
			count_dict[key] = 0
			sum_dict[key] = 0
		count_dict[key] += 1
		sum_dict[key] += value

	new_key_vec = []
	new_value_vec = []
	for key in count_dict:
		new_key_vec.append(float(key))
		new_value_vec.append( sum_dict[key] / count_dict[key] )

	return new_key_vec, new_value_vec

def plot_price():
# price_rating and recommendation prob.
	price_rating_vec, p_with_vec = aggregate_by_key(df['price_rating'], df['p_with'])

	fig = plt.figure(figsize=(5.6,3))
	ax = fig.add_axes([0.25, 0.28, 0.73, 0.7])

	ax.bar(price_rating_vec, p_with_vec, width=1, alpha=0.5, color='black')
	plt.ylim(0, 0.028)
	plt.xlim(0, 8)
	plt.xlabel('aspect score on price', weight='bold', fontsize=24)
	plt.ylabel('rec. prob.', weight='bold', fontsize=24)

	plt.savefig('images/price_rec_prob.png', dpi=1200)
	plt.savefig('images/price_rec_prob.eps', dpi=1200)

	plt.show()

def plot_rating():
# rating(star) and recommendation prob.
	stars_vec, p_with_vec = aggregate_by_key(df['stars'], df['p_with'])

	fig = plt.figure(figsize=(5.6,3))
	ax = fig.add_axes([0.25, 0.28, 0.73, 0.7])

	plt.bar(stars_vec, p_with_vec, width=0.25, alpha=0.5, color='black')
	plt.xlabel('rating scores (stars)', weight='bold', fontsize=24)
	plt.ylabel('rec. prob.', weight='bold', fontsize=24)

	plt.savefig('images/rating_rec_prob.png', dpi=1200)
	plt.savefig('images/rating_rec_prob.eps', dpi=1200)

	plt.show()


if __name__ == '__main__':
	plot_price()
	#plot_rating()
