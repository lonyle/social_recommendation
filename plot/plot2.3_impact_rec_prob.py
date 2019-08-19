import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)

import json

def plot_ImpRatio():
	fig = plt.figure()
	ax = fig.add_axes([0.17, 0.2, 0.78, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_rec_prob_profit.json'

	results = json.load(open(tmp_filename))

	rec_prob_vec = results['rec_prob_vec']

	strategy_vec = results['strategy_vec']

	improvement_ratio_vec = []
	for strategy in strategy_vec:
		improvement_ratio_vec.append( strategy['opt_profit']/strategy['baseline_profit'] - 1 )

	ax.plot(rec_prob_vec, improvement_ratio_vec, color='black', label='ImpRatio',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.xlabel('rec. prob. $q_i$ $(p_i=1,r_i=0)$', weight='bold')
	plt.ylabel('ImpRatio', weight='bold')

	plt.savefig('images/rec_prob_ImpRatio.eps', dpi=1200)

	plt.show()

def plot_price_change_ratio():
	fig = plt.figure()
	ax = fig.add_axes([0.17, 0.2, 0.78, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_rec_prob_profit.json'

	results = json.load(open(tmp_filename))

	rec_prob_vec = results['rec_prob_vec']

	strategy_vec = results['strategy_vec']

	price_change_ratio_vec = []
	for strategy in strategy_vec:
		price_change_ratio_vec.append( strategy['opt_price']/strategy['baseline_price'] - 1 )

	ax.plot(rec_prob_vec, price_change_ratio_vec, color='black', label='ImpRatio',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.xlabel('rec. prob. $q_i$ $(p_i=1,r_i=0)$', weight='bold')
	plt.ylabel('price change ratio', weight='bold')

	plt.savefig('images/rec_prob_price_change.eps', dpi=1200)

	plt.show()

def plot_social_value():
	fig = plt.figure()
	ax = fig.add_axes([0.16, 0.2, 0.78, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_rec_prob_profit.json'

	results = json.load(open(tmp_filename))

	rec_prob_vec = results['rec_prob_vec']

	strategy_vec = results['strategy_vec']

	social_value_vec = []
	baseline_social_value_vec = []
	diff_average_vec = []
	diff_recommender_vec = []
	diff_non_recommender_vec = []
	for strategy in strategy_vec:
		social_value_vec.append( strategy['average_price'] )
		baseline_social_value_vec.append(strategy['baseline_price'])
		diff_average_vec.append( -strategy['average_price']+strategy['baseline_price'] )
		diff_recommender_vec.append( -strategy['opt_price']+strategy['opt_reward'] + strategy['baseline_price'] )
		diff_non_recommender_vec.append( -strategy['opt_price'] + strategy['baseline_price'] )

	ax.plot(rec_prob_vec, diff_recommender_vec, '--', color='black', label='recommender',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(rec_prob_vec, diff_average_vec, color='black', label='average',\
		linewidth=3, marker='', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(rec_prob_vec, diff_non_recommender_vec, '--', color='black', label='non-recommender',\
		linewidth=3, marker='D', markersize=10, fillstyle='none', markeredgewidth=2)
	
	ax.plot(rec_prob_vec, np.zeros_like(rec_prob_vec), '--', color='black')

	# ax.plot(rec_prob_vec, social_value_vec, color='black', label='average price',\
	# 	linewidth=3, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)
	# ax.plot(rec_prob_vec, baseline_social_value_vec, '--', label='baseline price', color='black', linewidth=3)

	plt.xlabel('rec. prob. $q_i$ $(p_i=1,r_i=0)$', weight='bold')
	plt.ylabel('increase of utility', weight='bold')
	plt.legend(loc='upper right', fontsize=22, frameon=False)
	#plt.ylim(-5000, 13000)
	#plt.xlim(0, 0.15)

	plt.savefig('images/rec_prob_social_value.eps', dpi=1200)

	plt.show()

if __name__ == '__main__':
	plot_ImpRatio()
	plot_social_value()
	#plot_price_change_ratio()
