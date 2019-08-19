''' the common functions to do experiments
	In the result figure, we compare the profit of the following algorithms:
	1. optimal fixed strategy
	2. optimal mixed strategy
	3. thompson sampling
	4. q-learning
'''

import thompson_sampling
import numpy as np
import social_network
import baseline_fixed_action
import time_variant_mixed
import q_learning
import q_learning_big_transition
import degree_cutoff
import opt_mixed
import time_cutoff
import boost_cutoff
import influence_cutoff

import logging
import utils
import json

class Exp:
	def __init__(self):
		self.TS_influence_vec = []
		self.TS_q_learning_vec = []
		self.TS_mixed_vec = []

		self.q_learning_vec = []
		self.degree_cutoff_vec = []
		self.opt_fixed_vec = []
		self.opt_mixed_vec = []

		self.time_cutoff_vec = []
		self.influence_cutoff_vec = []
		self.boosted_cutoff_vec = []

		self.baseline_profit_vec = []
		self.param_vec = [] # this is for output

	def run_q_learning(self, delta, rec_prob_func, adopt_prob_func, default_weight_vec=None):
		num_sims = 2000
		if default_weight_vec:
			q_learning_big_transition.default_weight_vec = default_weight_vec
		average_profit = q_learning_big_transition.runner(delta, rec_prob_func, adopt_prob_func, num_sims)
		return average_profit

	def run_TS_q_learning(self, delta, rec_prob_func, adopt_prob_func):
		''' liye: shall we install the 
		'''
		method_name = 'q-learning'
		profit = thompson_sampling.runner(delta, rec_prob_func, adopt_prob_func, method_name)
		return profit

	def run_opt_fixed(self, delta, rec_prob_func, adopt_prob_func):
		action, profit = baseline_fixed_action.find_opt_action(delta, rec_prob_func, adopt_prob_func)
		return profit

	def get_baseline_profit(self, delta, rec_prob_func, adopt_prob_func):
		''' the optimal without reward (can adjust price)
		'''
		action, profit = baseline_fixed_action.find_opt_action_baseline(delta, rec_prob_func, adopt_prob_func)
		return profit

	def run_opt_mixed(self, delta, rec_prob_func, adopt_prob_func):
		opt_strategy, opt_profit = opt_mixed.find_opt_mixed_strategy(\
			delta, rec_prob_func, adopt_prob_func)
		return opt_strategy, opt_profit

	def run_TS_mixed(self, delta, rec_prob_func, adopt_prob_func):
		method_name = 'mixed'
		profit = thompson_sampling.runner(delta, rec_prob_func, adopt_prob_func, method_name)
		return profit

	def run_TS_influence(self, delta, rec_prob_func, adopt_prob_func):
		method_name = 'influence'
		profit = thompson_sampling.runner(delta, rec_prob_func, adopt_prob_func, method_name)
		return profit

	def run_degree_cutoff(self, delta, rec_prob_func, adopt_prob_func):
		opt_profit, opt_threshold = degree_cutoff.test_degree_threshold(delta, rec_prob_func, adopt_prob_func)
		return opt_profit

	def influence_different_k(self, delta, rec_prob_func, adopt_prob_func):
		# edited on 2019-05-29: run the algorithm for different k
		profit_vec, k_vec = influence_cutoff.test_influence_threshold(delta, rec_prob_func, adopt_prob_func, output_all_K=True)
		return profit_vec, k_vec

	def run_experiments(self, delta, rec_prob_func, adopt_prob_func):
		baseline_profit = self.get_baseline_profit(delta, rec_prob_func, adopt_prob_func)
		self.baseline_profit_vec.append( baseline_profit )

		opt_fixed_result = self.run_opt_fixed(delta, rec_prob_func, adopt_prob_func)
		self.opt_fixed_vec.append( opt_fixed_result )
		
		opt_mixed_strategy, opt_mixed_result = self.run_opt_mixed(delta, rec_prob_func, adopt_prob_func)
		self.opt_mixed_vec.append( opt_mixed_result )

		q_learning_result = self.run_q_learning(delta, rec_prob_func, adopt_prob_func, default_weight_vec=opt_mixed_strategy)
		self.q_learning_vec.append( q_learning_result )		

		opt_profit, opt_threshold = time_cutoff.test_time_threshold(delta, rec_prob_func, adopt_prob_func)
		self.time_cutoff_vec.append(opt_profit)

		degree_cutoff_result = self.run_degree_cutoff(delta, rec_prob_func, adopt_prob_func)
		self.degree_cutoff_vec.append( degree_cutoff_result )

	def run_experiments_TS(self, delta, rec_prob_func, adopt_prob_func):
		TS_q_learning_result = self.run_TS_q_learning(delta, rec_prob_func, adopt_prob_func)
		self.TS_q_learning_vec.append( TS_q_learning_result )

		TS_mixed_result = self.run_TS_mixed(delta, rec_prob_func, adopt_prob_func)
		self.TS_mixed_vec.append( TS_mixed_result )

		TS_influence_result = self.run_TS_influence(delta, rec_prob_func, adopt_prob_func)
		self.TS_influence_vec.append( TS_influence_result )

	def run_extra_experiments(self, delta, rec_prob_func, adopt_prob_func):
		''' run influence-threshold, time-cutoff, boosting-cutoff
		'''
		opt_profit, opt_k = influence_cutoff.test_influence_threshold(delta, rec_prob_func, adopt_prob_func)
		self.influence_cutoff_vec.append(opt_profit)

		# opt_profit, opt_k = boost_cutoff.test_boosted_threshold(delta, rec_prob_func, adopt_prob_func)
		# self.boosted_cutoff_vec.append(opt_profit)

	def dump_to_file(self, filename):
		result = {
			'q_learning_vec': self.q_learning_vec,			
			'opt_mixed_vec': self.opt_mixed_vec,
			'opt_fixed_vec': self.opt_fixed_vec,
			'degree_cutoff_vec': self.degree_cutoff_vec,
			'param_vec': self.param_vec,
			'baseline_profit_vec': self.baseline_profit_vec,

			'influence_cutoff_vec': self.influence_cutoff_vec,
			'time_cutoff_vec': self.time_cutoff_vec,
			'boosted_cutoff_vec': self.boosted_cutoff_vec
		}
		with open(filename, 'w') as output_file:
			json.dump(result, output_file, indent=4)

	def dump_to_file_TS(self, filename):
		tmp_result = {
			'TS_q_learning_vec': self.TS_q_learning_vec,
			'TS_influence_vec': self.TS_influence_vec,
			'TS_mixed_vec': self.TS_mixed_vec,
			'param_vec': self.param_vec
		}
		print (tmp_result)
		old_result = json.load(open(filename))
		old_count = old_result['count']
		# update the result: taking the average
		new_result = {}
		for key in old_result:
			if key == 'count':
				continue
			new_result[key] = []
			for i in range(len(old_result[key])):
				value = (old_result[key][i] * old_count + tmp_result[key][i]) / (old_count+1)
				new_result[key].append(value)

		new_result['count'] = old_count + 1
		with open(filename, 'w') as output_file:
			json.dump(new_result, output_file, indent=4)

