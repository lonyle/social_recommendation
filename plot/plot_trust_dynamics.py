import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 26}
matplotlib.rc('font', **font)
import numpy as np

import json

output_filename = 'data/result_trust_dynamics.json'

def plot_strategy():
	data = json.load(open(output_filename))
	reward_vec = data['reward_vec']
	profit_vec = data['profit_vec']
	price_vec = data['price_vec']

	iteration_vec = np.arange(len(reward_vec))

	plt.plot(iteration_vec, reward_vec, color='black', marker = 'o', label='opt. reward $r^*$')
	plt.plot(iteration_vec, price_vec, color='black', marker = 'x', label='opt. price $p^*$')
	plt.xlabel('iteration number')
	plt.legend()
	
	plt.savefig('images/trust_strategy_dynamics.eps', dpi=1200)
	plt.show()

def plot_trust():
	data = json.load(open(output_filename))
	reward_vec = data['reward_vec']
	profit_vec = data['profit_vec']
	price_vec = data['price_vec']
	trust_vec = data['trust_vec']

	iteration_vec = np.arange(len(reward_vec))

	plt.axes([0.18, 0.2, 0.78, 0.7])
	plt.plot(iteration_vec, trust_vec, color='black', linewidth=2, label='10 firms dynamics')
	plt.plot([0, 50], [1/1.267, 1/1.267], linestyle=(0, (3, 10, 1, 10)), color='black', linewidth=2, label='under single firm\'s\noptimal strategy')
	plt.xlabel('iteration')
	plt.ylabel('trust $\\tilde{\\tau}$')

	plt.legend(loc='upper right', fontsize=22, frameon=False)

	plt.savefig('images/trust_trust_dynamics.eps', dpi=1200)
	plt.show()

if __name__ == '__main__':
	#plot_strategy()
	plot_trust()