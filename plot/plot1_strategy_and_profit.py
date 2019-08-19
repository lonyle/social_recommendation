import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 24, 'weight': 'bold'}
matplotlib.rc('font', **font)
import numpy as np

import json

def plot_reward_and_profit():
	tmp_filename = 'data/result_reward_profit.json'
	results = json.load(open(tmp_filename))
	price_vec = results['price_vec']
	reward_vec = results['reward_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.15, 0.2, 0.8, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	marker_vec = ['o', 'x', 'D']
	marker_idx = 0
	for price in price_vec:
		ax.plot(reward_vec, results[str(price)], color='black', label='$p=$'+str(price), linewidth=2,\
			marker=marker_vec[marker_idx], markersize=10, fillstyle='none', markeredgewidth=2)
		marker_idx += 1

	plt.xlabel('the reward $r$', weight='bold')
	plt.ylabel('profit', weight='bold')
	
	plt.legend(loc='lower center', fontsize=20, frameon=False)

	plt.savefig('images/reward_and_profit.eps', dpi=1200)

	plt.show()

def plot_price_and_profit():
	tmp_filename = 'data/result_price_profit.json'
	results = json.load(open(tmp_filename))
	price_vec = results['price_vec']
	reward_vec = results['reward_vec']

	fig = plt.figure()
	ax = fig.add_axes([0.17, 0.2, 0.78, 0.7])
	ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

	marker_vec = ['o', 'x', 'D']
	marker_idx = 0
	for reward in reward_vec:
		plt.plot(price_vec, results[str(reward)], color='black', label='$r=$'+str(reward), linewidth=2,\
			marker=marker_vec[marker_idx], markersize=10, fillstyle='none', markeredgewidth=2)
		marker_idx += 1

	plt.xlabel('the price $p$', weight='bold')
	plt.ylabel('profit', weight='bold')
	plt.ylim(-26000, 32000)
	plt.legend(loc='lower center', fontsize=20, frameon=False)

	plt.savefig('images/price_and_profit.eps', dpi=1200)

	plt.show()

if __name__ == '__main__':
	#plot_reward_and_profit()
	plot_price_and_profit()