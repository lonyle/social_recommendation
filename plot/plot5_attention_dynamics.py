import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 24, 'weight': 'bold'}
matplotlib.rc('font', **font)
import numpy as np

import json

output_filename = 'data/result_attention_dynamics.json'

def plot_strategy():
	data = json.load(open(output_filename))
	reward_vec = data['reward_vec']
	profit_vec = data['profit_vec']
	price_vec = data['price_vec']
	attention_scale_vec = data['attention_scale_vec']

	iteration_vec = np.arange(len(reward_vec))

	fig = plt.figure()
	ax = fig.add_axes([0.22, 0.2, 0.75, 0.7])

	ax.plot(iteration_vec, reward_vec, color='black', label='opt. reward $r^*$')
	ax.plot(iteration_vec, price_vec, color='black', label='opt. price $p^*$')
	plt.xlabel('iteration number')
	plt.legend()
	
	plt.savefig('images/attention_strategy_dynamics.eps', dpi=1200)
	plt.show()

def plot_profit():
	data = json.load(open(output_filename))
	reward_vec = data['reward_vec']
	profit_vec = data['profit_vec']
	price_vec = data['price_vec']
	attention_scale_vec = data['attention_scale_vec']

	iteration_vec = np.arange(len(reward_vec))


	plt.axes([0.15, 0.2, 0.8, 0.7])
	plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
	plt.plot(iteration_vec[1:], profit_vec[1:], color='black', linewidth=3, label='10 firms dynamics')
	plt.plot([0, 50], [16275.6249153, 16275.6249153], '--', color='black', linewidth=2, label='single firm optimal')

	plt.legend(loc='upper right', fontsize=24, frameon=False)

	plt.xlabel('iteration', weight='bold')
	plt.ylabel('profit', weight='bold')
	plt.ylim(0, 40000)

	plt.savefig('images/attention_profit_dynamics.eps', dpi=1200)
	plt.show()

	# plt.plot(iteration_vec, attention_scale_vec, color='black')
	# plt.xlabel('iteration')
	# plt.ylabel('prob. that a recommendation is received')
	# plt.savefig('images/attention_scale_dynamics.eps', dpi=5000)
	# plt.show()

if __name__ == '__main__':
	#plot_strategy()
	plot_profit()