''' using time as the cutoff-point
	when the number of rounds is above a certain threshold
'''

import evaluate
import utils
import social_network
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('time-cutoff')

def get_decision_func(threshold):
	def decision_func(state_param):
		''' m+n is the number of users who already arrive
			when m+n is small, choose the state with large reward
			when m+n is larger than a threshold (e.g. 2000), choose zero reward
		'''
		m, delta_m, n, delta_n = state_param
		if m+n < threshold:
			return utils.mixed_actions[1]
		else:
			return utils.mixed_actions[0]
	return decision_func

def test_time_threshold(delta, rec_prob_func, adopt_prob_func):
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)
	if utils.graph_name == 'Facebook':
		threshold_vec = range(100, 3000, 250)
	elif utils.graph_name == 'Yelp':
		threshold_vec = range(1000, 80000, 5000)
	opt_profit = -1
	opt_threshold = None
	for threshold in threshold_vec:
		decision_func = get_decision_func(threshold)
		average_profit = evaluate.evaluate_average(graph, decision_func, 200)
		logger.info('average_profit: %f, threshold: %d'%(average_profit, threshold))
		if average_profit > opt_profit:
			opt_profit = average_profit
			opt_threshold = threshold
	return opt_profit, opt_threshold

if __name__ == '__main__':
	opt_profit, opt_threshold = test_time_threshold(0.1, utils.true_rec_prob_func, utils.true_adopt_prob_func)
	logger.info('opt_profit: %f, opt_threshold:%d'%(opt_profit, opt_threshold))