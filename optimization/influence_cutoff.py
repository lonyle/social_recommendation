''' created on 2019-01-25, copied from degree_cutoff.py
'''

import evaluate
import social_network
import utils
import logging
import random 
import subprocess
import os.path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('influence-cutoff')

selected_nodes = set() # the nodes selected by IM, loaded into memory to speed up

ROUND_PEDGE = False # whether we only use nearby p-edge, used by thompson_sampling

def get_decision_func_influence(k, rec_prob_func):
	reward_action = utils.possible_actions[-1] # the rewarding action
	no_reward_action = utils.possible_actions[0] # the no-reward action

	# run the IM algorithm, get the k nodes into a file
	pedge = rec_prob_func(no_reward_action['price'], no_reward_action['reward']) 
	if ROUND_PEDGE == True:
		pedge = max(round(pedge*25)/25, 0.04) # round to 0.04

	# the influence probability is the probability for a receiver to make recommendation without reward
	''' comment: I guess here, we should apply the boosting influence algorithm '''

	output_filename = '/home/liye/Code/OPIM/OPIM1.1/result/seed/' + 'seed_facebook_opim-c_minBound_k'+str(k)+'_UNI'+"{:.6f}".format(pedge)

	while os.path.exists(output_filename) == False:
		subprocess.call(['./OPIM1.1.o', '-func=1', '-gname=facebook', '-alg=opim-c',\
			 '-seedsize='+str(k), '-eps=0.01', '-model=IC', '-pdist=UNI', '-pedge='+str(pedge)], cwd='/home/liye/Code/OPIM/OPIM1.1/')

	selected_nodes = set() # reset the set
	for line in open(output_filename):
		node = line.strip()
		selected_nodes.add(node)

	# Note: we only consider two actions, either reward or not
	def decision_func(current_state_param, node_feature):
		if node_feature['id'] in selected_nodes:
			action = reward_action
		else:
			action = no_reward_action
		return action
	return decision_func

def test_influence_threshold(delta,
				 			 rec_prob_func, 
				 			 adopt_prob_func,
				 			 output_all_K=False):
	''' greedily find k nodes whose influence scores are highest
	'''
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)

	k_vec = range(100, 3000, 300)#range(100, 3000, 300)
	opt_profit = -1
	opt_k = None
	profit_vec = []
	for k in k_vec:
		decision_func = get_decision_func_influence(k, graph.rec_prob_func)
		average_profit = evaluate.evaluate_average(graph, decision_func, 200, is_node_feature=True)
		logger.info('average_profit: %f, k: %d'%(average_profit, k))
		profit_vec.append(average_profit)
		if average_profit > opt_profit:
			opt_profit = average_profit
			opt_k = k
	if output_all_K == True:
		return profit_vec, k_vec
	return opt_profit, opt_k

def find_decision_func(num_sims, delta, adopt_rec_prob_dict):
	def rec_prob_func(price, reward):
		action_key = utils.action_to_key({'price': price, 'reward': reward})
		return adopt_rec_prob_dict['recommend'][action_key]

	def adopt_prob_func(price, reward):
		action_key = utils.action_to_key({'price': price, 'reward': reward})
		return adopt_rec_prob_dict['adopt'][action_key] 

	opt_profit, opt_k = test_influence_threshold(delta, rec_prob_func, adopt_prob_func)

	return get_decision_func_influence(opt_k, rec_prob_func)

if __name__ == '__main__':
	opt_profit, opt_k = test_influence_threshold(utils.true_delta, utils.true_rec_prob_func, utils.true_adopt_prob_func)
	logger.info('opt_profit: %f, opt_k:%d'%(opt_profit, opt_k))