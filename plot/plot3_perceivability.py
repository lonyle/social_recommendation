import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 24, 'weight': 'bold'}
matplotlib.rc('font', **font)
import numpy as np

import json

def plot_perceibability_strategy():
	# trust = 0.5
	tmp_filename = 'data/result_perceivability_opt_strategy2.json'

	results = json.load(open(tmp_filename))

	gamma_vec = results['gamma_vec']

	strategy_vec = results['strategy_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.15, 0.18, 0.8, 0.7])

	opt_price_vec = []
	for strategy in strategy_vec:
		opt_price_vec.append( strategy['opt_price'] - 1 ) # the change of price
	ax.plot(gamma_vec, opt_price_vec, color='black', label='price $p^*-1$',\
		linewidth=2, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)

	opt_reward_vec = []
	for strategy in strategy_vec:
		opt_reward_vec.append( strategy['opt_reward'] )
	ax.plot(gamma_vec, opt_reward_vec, color='black', label='reward $r^*-0$',\
		linewidth=2, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)

	plt.legend(loc='lower center', fontsize=22, frameon=False)
	plt.xlabel('perceivability $\\gamma$', weight='bold')
	plt.ylabel('change of price/reward', weight='bold')
	plt.ylim(0, 3)
	plt.legend(loc='upper right', fontsize=22, frameon=False)

	plt.savefig('images/perceivability_strategy.eps', dpi=1200)
	plt.show()

def plot_perceibability_profit():
	#trust_vec = [0.5, 1, 2]
	trust_vec = [0]

	fig = plt.figure()
	ax = fig.add_axes([0.18, 0.2, 0.77, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	marker_vec = ['o', 'x', 'D']
	marker_idx = 0	
	for trust in trust_vec:
		tmp_filename = 'data/result_perceivability_opt_strategy'+str(trust)+'.json'

		results = json.load(open(tmp_filename))

		gamma_vec = results['gamma_vec']

		strategy_vec = results['strategy_vec']

		improvement_ratio_vec = []
		for strategy in strategy_vec:
			improvement_ratio_vec.append( strategy['opt_profit']/strategy['baseline_profit'] - 1 )
		ax.plot(gamma_vec, improvement_ratio_vec, color='black', label='trust $\\tau=$'+str(trust),\
			linewidth=3, marker=marker_vec[marker_idx], markersize=10, fillstyle='none', markeredgewidth=2)
		marker_idx += 1
		
	plt.xlabel('perceivability $\\gamma$', weight='bold')
	plt.legend(loc='upper right', fontsize=22, frameon=False)
	plt.ylabel('ImpRatio', weight='bold')
	#plt.ylim(0.08, 0.88)

	plt.savefig('images/perceivability_profit.eps', dpi=1200)
	plt.show()

def plot_perceibability_social_value():
	trust_vec = [0]

	fig = plt.figure()
	ax = fig.add_axes([0.16, 0.2, 0.81, 0.7])
	
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	marker_vec = ['o', 'x', 'D']
	marker_idx = 0	
	for trust in trust_vec:
		tmp_filename = 'data/result_perceivability_opt_strategy'+str(trust)+'.json'

		results = json.load(open(tmp_filename))

		gamma_vec = results['gamma_vec']

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

		ax.plot(gamma_vec, diff_recommender_vec, '--', color='black', label='recommender',\
			linewidth=3, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
		ax.plot(gamma_vec, diff_average_vec, color='black', label='average',\
			linewidth=3, marker='', markersize=10, fillstyle='none', markeredgewidth=2)
		ax.plot(gamma_vec, diff_non_recommender_vec, '--', color='black', label='non-\nrecommender',\
			linewidth=3, marker='D', markersize=10, fillstyle='none', markeredgewidth=2)
		
		ax.plot(gamma_vec, np.zeros_like(gamma_vec), '--', color='black')


		# ax.plot(gamma_vec, social_value_vec, color='black', label='average price',\
		# 	linewidth=3, marker=marker_vec[marker_idx], markersize=10, fillstyle='none', markeredgewidth=2)
		# ax.plot(gamma_vec, baseline_social_value_vec, '--', label='baseline price', color='black', linewidth=3)

		marker_idx += 1
		
	plt.xlabel('perceivability $\\gamma_i$', weight='bold')
	plt.legend(loc='lower right', fontsize=19, frameon=False)
	plt.ylabel('increase of utility', weight='bold')
	#plt.ylim(-22000, 5000)
	plt.ylim(-2.3, 0.4)
	#plt.xlim(0.48,1)
	plt.xticks([0.5, 0.75, 1.0])
	plt.savefig('images/perceivability_social_value.eps', dpi=1200)
	plt.show()
	

if __name__ == '__main__':
	#plot_perceibability_profit()
	plot_perceibability_social_value()