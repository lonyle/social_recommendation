''' created on 2019-01-18: do not reuse the code for time_variant_mixed, because we do not want to copy the simulator
'''

import numpy as np
import social_network
import logging
import utils
import copy
import random
import time_variant_mixed

class StartingGraph(time_variant_mixed.RemainingGraph):
	def __init__(self, delta, rec_prob_func, adopt_prob_func):
		self.graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)

	def reset_remaining(self):
		self.graph.reset() # only reset the graph is good enough

### the following two functions are added on 2019-01-09
### edited on 2019-01-18: reduce the memory usage, by only constructing one graph
def find_opt_mixed_strategy(delta, rec_prob_func, adopt_prob_func, num_sims=100):
	''' do not consider the time-variant strategy, find the optimal mixed strategy starting from the beginning
	'''
	graph = StartingGraph(delta, rec_prob_func, adopt_prob_func) # when no simulator is runned, we want to release the memory
	opt_strategy, opt_profit, _ = graph.opt_strategy_graph(num_sims)
	return opt_strategy, opt_profit

def find_decision_func(num_sims, delta, adopt_rec_prob_dict):
	def rec_prob_func(price, reward):
		action_key = utils.action_to_key({'price': price, 'reward': reward})
		return adopt_rec_prob_dict['recommend'][action_key]

	def adopt_prob_func(price, reward):
		action_key = utils.action_to_key({'price': price, 'reward': reward})
		return adopt_rec_prob_dict['adopt'][action_key] 

	opt_strategy, opt_profit = find_opt_mixed_strategy(delta, rec_prob_func, adopt_prob_func)

	def decision_func(state_param):
		return time_variant_mixed.my_random_choice(utils.mixed_actions, opt_strategy)

	return decision_func

if __name__ == '__main__':
	opt_strategy, opt_profit = find_opt_mixed_strategy(utils.true_delta, utils.true_rec_prob_func, utils.true_adopt_prob_func, 200)
	print ('opt_strategy:', opt_strategy, 'opt_profit:', opt_profit)