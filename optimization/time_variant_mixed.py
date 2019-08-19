''' time variant strategy: at the beginning of each epoch, find the optimal strategy for the remaining graph
	edited on 2019-01-08: add mixed strategy
'''

import numpy as np
import social_network
import logging
import utils
import copy
import random

EPOCH_SIZE = 10000 # if the epoch size is large enough, only consider one mixed strategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('time_variant')

def my_random_choice(actions, strategy):
	rand = random.random()
	sum_ = 0
	for i in range(len(actions)):
		sum_ += strategy[i]
		if rand < sum_:
			return actions[i]

class RemainingGraph():
	def __init__(self, simulator):
		self.graph = social_network.Graph(simulator.delta, simulator.rec_prob_func, simulator.adopt_prob_func)
		self.simulator = simulator

	def reset_remaining(self):
		# set the reseted parameters to what simulator have
		self.graph.is_recommended = dict(self.simulator.is_recommended)
		self.graph.N_is_recommended = self.simulator.N_is_recommended
		self.graph.already_other_info_set = set(self.simulator.already_other_info_set)
		self.graph.later_other_info = list(self.simulator.later_other_info)
		self.graph.later_other_info_set = set(self.simulator.later_other_info_set)
		self.graph.newly_recommended_set = set(self.simulator.newly_recommended_set)
		self.graph.n = self.simulator.n

		self.graph.cost_on_reward = 0
		self.graph.gross_profit = 0

	def opt_strategy_graph(self, num_sims, baseline_strategy=None):
		''' the opt. strategy for a remaining graph
		'''
		opt_profit = -1
		opt_action = None
		baseline_profit = None
		for strategy in utils.possible_strategies:
			def decision_func():
				action = my_random_choice(utils.mixed_actions, strategy)
				return action
			average_profit = self.evaluate_remaining(decision_func, num_sims)
			if baseline_strategy:
				if strategy == baseline_strategy:
					baseline_profit = average_profit
			print('strategy:', strategy, 'average_profit:', average_profit)
			if average_profit > opt_profit:
				opt_profit = average_profit
				opt_strategy = strategy

		improvement = opt_profit - baseline_profit if baseline_strategy else 0
		return opt_strategy, opt_profit, improvement

	def evaluate_remaining(self, decision_func, num_sims): # the action is changed to decision_func to allow randomized strategies
		total_profit_vec = []
		for n in range(num_sims):
			total_profit = self.evaluate_remaining_once(decision_func)
			total_profit_vec.append(total_profit)
		return sum(total_profit_vec)/len(total_profit_vec)

	def evaluate_remaining_once(self, decision_func):
		self.reset_remaining() # reset to the remaining graph
		while True:
			action = decision_func()
			self.graph.next(action)
			current_state_param = self.graph.current_state_param()
			m, delta_m, n, delta_n = current_state_param
			if delta_m + delta_n == 0: # no more potential users to be informed
				break

		total_profit = self.graph.gross_profit - self.graph.cost_on_reward

		return total_profit

def run_epoches(num_sims, delta, rec_prob_func, adopt_prob_func):
	''' run the simulators epoch-by-epoch
	'''
	simulator = social_network.Graph(delta, rec_prob_func, adopt_prob_func)
	epoch_count = 0
	baseline_strategy = None
	improvement_vec = []
	while simulator.is_terminated() == False:
		epoch_count += 1
		logger.info('epoch %d'%(epoch_count))
		epoch_size = EPOCH_SIZE

		# with open('data/time_variant.pydata', 'wb') as output_file:
		# 	pickle.dump(simulator, output_file)

		remaining_graph = RemainingGraph(simulator) # construct the remaining graph according to the simulator
		strategy, profit, improvement = remaining_graph.opt_strategy_graph(num_sims, baseline_strategy)
		if baseline_strategy == None:
			baseline_strategy = strategy
		
		improvement_vec.append(improvement)

		print ('the optimal strategy in the remaining graph is:', strategy, 'opt. profit:', profit)

		for i in range(epoch_size):
			#logger.info('epoch %d, iteration %d'%(epoch_count, i))
			state_param = simulator.current_state_param()
			action = my_random_choice(utils.mixed_actions, strategy)
			simulator.next(action)
			if simulator.is_terminated(): # in the epoch, is stopped, terminate
				break

	profit = simulator.gross_profit - simulator.cost_on_reward
	return profit, improvement_vec



if __name__ == '__main__':
	profit, improvement_vec = run_epoches(200, utils.true_delta, utils.true_rec_prob_func, utils.true_adopt_prob_func) # 200 iterations for each mixed strategy
	print ('the one-shot profit is:', profit)
	print ('the improvement_vec is:', improvement_vec)