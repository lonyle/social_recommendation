import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)

import json


def plot_ImpRatio_profit():
	fig = plt.figure()
	ax = fig.add_axes([0.22, 0.2, 0.73, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_info_prob_profit.json'

	results = json.load(open(tmp_filename))

	info_prob_vec = results['info_prob_vec']

	strategy_vec = results['strategy_vec']

	improvement_ratio_vec = []
	for strategy in strategy_vec:
		improvement_ratio_vec.append( strategy['opt_profit']/strategy['baseline_profit'] - 1 )

	ax.plot(info_prob_vec, improvement_ratio_vec, color='black', label='ImpRatio',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.xlabel('initially informed prob. $\\delta_i$', weight='bold')
	plt.ylabel('ImpRatio', weight='bold')
	#plt.ylim(-49000, 130000)

	plt.savefig('images/initial_info_prob_ImpRatio.eps', dpi=1200)

	plt.show()

def plot_ImpRatio_social_value():
	fig = plt.figure()
	ax = fig.add_axes([0.21, 0.2, 0.75, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_info_prob_profit.json'

	results = json.load(open(tmp_filename))

	info_prob_vec = results['info_prob_vec']

	strategy_vec = results['strategy_vec']

	social_value_vec = []
	baseline_social_value_vec = []
	diff_average_vec = []
	diff_recommender_vec = []
	diff_non_recommender_vec = []
	for strategy in strategy_vec:
		social_value_vec.append( strategy['average_price'] )
		baseline_social_value_vec.append( strategy['baseline_price'] )
		diff_average_vec.append( -strategy['average_price']+strategy['baseline_price'] )
		diff_recommender_vec.append( -strategy['opt_price']+strategy['opt_reward'] + strategy['baseline_price'] )
		diff_non_recommender_vec.append( -strategy['opt_price'] + strategy['baseline_price'] )

	ax.plot(info_prob_vec, diff_recommender_vec, '--', color='black', label='recommender',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(info_prob_vec, diff_average_vec, color='black', label='average',\
		linewidth=3, marker='', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(info_prob_vec, diff_non_recommender_vec, '--', color='black', label='non-recommender',\
		linewidth=3, marker='D', markersize=10, fillstyle='none', markeredgewidth=2)
	
	ax.plot(info_prob_vec, np.zeros_like(info_prob_vec), '--', color='black')

	# ax.plot(info_prob_vec, social_value_vec, color='black', label='average price',\
	# 	linewidth=3, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)
	# ax.plot(info_prob_vec, baseline_social_value_vec, '--', label='baseline price', color='black', linewidth=3)

	plt.xlabel('initially informed prob. $\\delta_i$', weight='bold')
	plt.ylabel('increase of utility', weight='bold')
	#plt.ylim(0.25, 1.7)
	plt.ylim(-1.5, 0.75)
	plt.legend(loc='lower right', fontsize=22, frameon=False)

	plt.savefig('images/initial_info_prob_social_value.eps', dpi=1200)

	plt.show()

def plot_price_change_ratio():
	fig = plt.figure()
	ax = fig.add_axes([0.22, 0.2, 0.73, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	tmp_filename = 'data/result_initial_info_prob_profit.json'

	results = json.load(open(tmp_filename))

	info_prob_vec = results['info_prob_vec']

	strategy_vec = results['strategy_vec']

	price_change_ratio_vec = []
	for strategy in strategy_vec:
		price_change_ratio_vec.append( strategy['opt_price']/strategy['baseline_price'] - 1 )

	ax.plot(info_prob_vec, price_change_ratio_vec, color='black', label='ImpRatio',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.xlabel('initially informed prob. $\\delta$', weight='bold')
	plt.ylabel('price change ratio', weight='bold')
	#plt.ylim(-49000, 130000)

	plt.savefig('images/initial_info_prob_price_change.eps', dpi=1200)

	plt.show()

if __name__ == '__main__':
	plot_ImpRatio_profit()
	plot_ImpRatio_social_value()
	#plot_price_change_ratio()