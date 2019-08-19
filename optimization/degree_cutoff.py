''' the strategy is cut-off by the degree (or some other score) of users
	the reward is only given to those users with a score higher than a threshold
	three kinds of metric: degree, centrality, influence
	for influence, the cut-off is the budget size. For a certain budget-size, the selected users are given reward if they show up
'''

''' 2019-01-08
	firstly, we do not consider time-variant strategies
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
logger = logging.getLogger('degree-cutoff')

selected_nodes = set() # the nodes selected by IM, loaded into memory to speed up

def get_decision_func(threshold):
	''' return the decision function for a given threshold
	'''
	def decision_func(current_state_param, node_feature): # add the input of features of the selected node
		if node_feature['degree'] == None: # this is because the node is empty
			return random.choice(utils.possible_actions)
		if node_feature['degree'] > threshold:
			action = utils.mixed_actions[-1] # the action with the highest reward
		else:
			action = utils.mixed_actions[0]
		return action
	return decision_func

def test_degree_threshold(delta, rec_prob_func, adopt_prob_func):
	''' test different degree threshold
	'''
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)
	#threshold_vec = [20, 50, 100, 150, 200]
	threshold_vec = range(30, 50, 2)
	opt_profit = -1
	opt_threshold = None
	for threshold in threshold_vec:
		decision_func = get_decision_func(threshold)
		average_profit = evaluate.evaluate_average(graph, decision_func, 200, is_node_feature=True)
		logger.info('average_profit: %f, threshold: %d'%(average_profit, threshold))
		if average_profit > opt_profit:
			opt_profit = average_profit
			opt_threshold = threshold
	return opt_profit, opt_threshold


if __name__ == '__main__':
	opt_profit, opt_threshold = test_degree_threshold(utils.true_delta, utils.true_rec_prob_func, utils.true_adopt_prob_func)
	logger.info('opt_profit: %f, opt_threshold:%d'%(opt_profit, opt_threshold))


