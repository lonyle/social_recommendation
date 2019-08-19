import matplotlib.pyplot as plt
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)
import numpy as np

import json


def plot_social_value_strategy():
	tmp_filename = 'data/result_social_value_opt_strategy.json'
	results = json.load(open(tmp_filename))

	eta_vec = results['eta_vec']

	strategy_vec = results['strategy_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.25, 0.2, 0.73, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	opt_price_vec = []
	for strategy in strategy_vec:
		opt_price_vec.append( strategy['opt_price'] -1 ) # change of price
	plt.plot(eta_vec, opt_price_vec, color='black', label='price $p^*-1$', \
		linewidth=2, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	opt_reward_vec = []
	for strategy in strategy_vec:
		opt_reward_vec.append( strategy['opt_reward'] )
	plt.plot(eta_vec, opt_reward_vec, color='black', label='reward $r^*-0$', \
		linewidth=2, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.xlabel('$\\eta$: scale of social value', weight='bold')
	plt.yticks(fontsize=22)
	plt.legend(loc='upper right', fontsize=22, frameon=False)
	plt.ylabel('change of price/reward', weight='bold')

	plt.savefig('images/social_value_strategy.eps', dpi=1200)
	plt.show()

def plot_ImpRatio():
	tmp_filename = 'data/result_social_value_opt_strategy.json'
	results = json.load(open(tmp_filename))

	eta_vec = results['eta_vec']

	strategy_vec = results['strategy_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.22, 0.2, 0.75, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	improvement_ratio_vec = []
	social_value_vec = []
	for strategy in strategy_vec:
		improvement_ratio_vec.append( strategy['opt_profit']/strategy['baseline_profit'] -1 )
		social_value_vec.append( strategy['social_value'] )
	ax.plot(eta_vec, improvement_ratio_vec, color='black', label='ImpRatio',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
	# ax.plot(eta_vec, social_value_vec, color='black', label='total social value',\
	# 	linewidth=2, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)
	plt.xlabel('$\\eta$: scale of social value', weight='bold')
	plt.ylabel('ImpRatio', weight='bold')
	#plt.legend(loc='upper left', fontsize=22, frameon=False)

	plt.savefig('images/social_value_ImpRatio.eps', dpi=1200)
	plt.show()

def plot_social_value():
	tmp_filename = 'data/result_social_value_opt_strategy.json'
	results = json.load(open(tmp_filename))

	eta_vec = results['eta_vec']

	strategy_vec = results['strategy_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.22, 0.2, 0.77, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

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

	ax.plot(eta_vec, diff_recommender_vec, '--', color='black', label='recommender',\
		linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(eta_vec, diff_average_vec, color='black', label='average',\
		linewidth=3, marker='', markersize=10, fillstyle='none', markeredgewidth=2)
	ax.plot(eta_vec, diff_non_recommender_vec, '--', color='black', label='non-\nrecommender',\
		linewidth=3, marker='D', markersize=10, fillstyle='none', markeredgewidth=2)
	
	ax.plot(eta_vec, np.zeros_like(eta_vec), '--', color='black')

	# ax.plot(eta_vec[:-1], social_value_vec[:-1], color='black', label='average price',\
	# 	linewidth=3, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)
	# ax.plot(eta_vec[:-1], baseline_social_value_vec[:-1], '--', label='baseline price', color='black', linewidth=3)

	plt.xlabel('scale of social value $\\eta$', weight='bold')
	plt.ylabel('increase of utility', weight='bold')
	plt.legend(loc='lower right', fontsize=19, frameon=False)
	plt.ylim(-0.8, 0.3)
	plt.yticks([-0.6, -0.4, -0.2, 0, 0.2])
	plt.savefig('images/social_value_total.eps', dpi=1200)
	plt.show()

if __name__ == '__main__':
	#plot_ImpRatio()
	plot_social_value()