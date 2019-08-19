''' optimization over Wechat's items
	the baseline is the current strategy, and the current recommendation probability with reward
	we need to assume the conterfactual recommendation probability
	there are two actions: orginal action (giving rewards), and no-reward
	we want to know the improvement by the mixed strategy (and other strategies)

	because we do not have the graph, we can only test the optimal mixed strategy
'''

import exp_utils

def run_one_firm(firm_param):
	exp_runner = exp_utils.Exp()
	delta = firm_param['other_info_prob']
	def rec_prob_func(price, reward):
		if reward == firm_param['old_reward']:
			rec_prob = firm_param['rec_prob']
		else:
			rec_prob = # infer the prob by the linear regression?
		return rec_prob
	def adopt_prob_func(price, reward):
		return firm_param['adopt_prob']

	utils.possible_reward = [0, firm_param['old_reward']]
	utils.reset_possible_actions()

	exp_runner.run_experiments(delta, rec_prob_func, adopt_prob_func)
