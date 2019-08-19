''' find the cut-off influence on the boosted influence 
'''

import math
import numpy as np
import evaluate
import social_network
import utils
import random 
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('boost-cutoff')

dir_name = '/home/liye/Code/BoostingInformationSpread/'
graph_filename = dir_name + 'dataset/facebook'
graph_prob_filename = dir_name + 'dataset/facebook_prob'
seeds_filename = dir_name + 'dataset/facebook_seeds.txt'
boosted_nodes_filename = dir_name + 'boosted_nodes.txt'

def add_inf_prob_uniform(prob):
	input_filename = graph_filename
	output_filename = graph_prob_filename
	with open(output_filename, 'w') as output_file:
		head = True
		for line in open(input_filename):
			if head == True:
				new_line = line
				head = False
			else:
				new_line = line.strip() + '\t' + str(prob) + '\n'

			output_file.write(new_line)
	
def gen_seed_file(delta):
	output_filename = seeds_filename
	N_nodes = 4039
	seeds = np.random.choice(N_nodes, int(delta*N_nodes)) 
	with open(output_filename, 'w') as output_file:
		for seed in seeds:
			output_file.write(str(seed) + '\n')

def get_decision_func(k, delta, rec_prob_func):
	reward_action = utils.possible_actions[-1]
	no_reward_action = utils.possible_actions[0]

	rec_prob_reward = rec_prob_func(reward_action['price'], reward_action['reward'])
	rec_prob_no_reward = rec_prob_func(reward_action['price'], reward_action['reward'])

	beta = math.log(1-rec_prob_reward) / math.log(1-rec_prob_no_reward)

	# process the graph file, and add the diffusion probability
	add_inf_prob_uniform(rec_prob_no_reward)

	# generate some seed nodes according to the initial informed prob
	gen_seed_file(delta*rec_prob_reward) # not all the informed nodes could be seed nodes

	# ./bin/prrboost dataset/facebook_prob dataset/facebook_seeds.txt beta k epsilon log_prrboost.txt log_prrboost_lbtest.txt
	epsilon = 0.1
	subprocess.call(['./bin/prrboost', 'dataset/facebook_prob', 'dataset/facebook_seeds.txt', str(beta),\
		str(k), str(epsilon), 'log_prrboost.txt', 'log_prrboost_lbtest.txt'],\
		cwd=dir_name)

	boosted_nodes = set()
	for line in open(boosted_nodes_filename):
		node = line.strip()
		boosted_nodes.add(node)

	def decision_func(current_state_param, node_feature):
		if node_feature['id'] in boosted_nodes:
			action = reward_action
		else:
			action = no_reward_action
		return action
	return decision_func

def test_boosted_threshold(delta, rec_prob_func, adopt_prob_func):
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)

	k_vec = range(1500, 2500, 400)
	opt_profit = -1
	opt_k = None
	for k in k_vec:
		decision_func = get_decision_func(k, graph.delta, graph.rec_prob_func)
		average_profit = evaluate.evaluate_average(graph, decision_func, 200, is_node_feature=True)
		logger.info('average_profit: %f, k: %d'%(average_profit, k))
		if average_profit > opt_profit:
			opt_profit = average_profit
			opt_k = k
	return opt_profit, opt_k


if __name__ == '__main__':
	opt_profit, opt_k = test_boosted_threshold()
	logger.info('opt_profit: %f, opt_k:%d'%(opt_profit, opt_k))