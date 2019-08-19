# only use the single action, what is the expected profit of baseline decision
import social_network
import evaluate
import utils

default_action = None

# possible_reward = [0.0, 0.1, 0.2, 0.3]# action space
# possible_price = [0.9, 1.0, 1.1]# action space

def baseline_decision(state_param): 
	''' decision is an algorithm that maps a state (specially, state_param) to action
	'''
	return default_action

def find_opt_action(delta, rec_prob_func, adopt_prob_func):
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)
	opt_profit = -1
	opt_action = None
	for price in utils.possible_price:
		for reward in utils.possible_reward:
			global default_action
			default_action = {'price': price, 'reward': reward}
			average_profit = evaluate.evaluate_average(graph, baseline_decision, 100)
			print (default_action, '\t|\t', average_profit)
			if average_profit > opt_profit:
				opt_profit = average_profit
				opt_action = default_action
	return opt_action, opt_profit

def find_opt_action_baseline(delta, rec_prob_func, adopt_prob_func):
	# the baseline action without rewards
	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)
	opt_profit = -1
	opt_action = None
	for price in utils.possible_price:
		global default_action
		default_action = {'price': price, 'reward': 0}
		average_profit = evaluate.evaluate_average(graph, baseline_decision, 100)
		print (default_action, '\t|\t', average_profit)
		if average_profit > opt_profit:
			opt_profit = average_profit
			opt_action = default_action
	return opt_action, opt_profit

if __name__ == '__main__':
	delta = 0.1

	# def rec_prob_func(price, reward):
	# 	rec_prob = 0.1 + 0.2 * reward 
	# 	return rec_prob

	# def adopt_prob_func(price, reward):
	# 	adopt_prob = 0.1 + 0.1 * (1-price)
	# 	return adopt_prob

	def rec_prob_func(price, reward):
		######### the working param ########
		## rec_prob = 0.02 + 0.3 * reward
		####################################
		if reward == 0.5:
			rec_prob = 0.2
		elif reward == 0.25:
			rec_prob = 0.11
		else:
			rec_prob = 0.02		
		return rec_prob * 5

	def adopt_prob_func(price, reward):
		######### the working param ########
		## adopt_prob = 0.1 + 0.2 * (1-price)
		####################################
		adopt_prob =  0.2
		# adopt_prob = 0.0189 + 0.008406 * (1-price)
		# adopt_prob *= 5
		return adopt_prob

	opt_action, opt_profit = find_opt_action(delta, rec_prob_func, adopt_prob_func)
	print ('opt_action:', opt_action, 'opt_profit:', opt_profit)


''' recording the results
 for Yelp data: (baseline parameters, delta=0.01)
 	{'reward': 0, 'price': 1}       |        6267.72
	{'reward': 0.25, 'price': 1}    |        17163.8875
	{'reward': 0.5, 'price': 1}     |        4725.11
 for Facebook data: (baseline parameters, delta=0.01)
 	{'price': 1, 'reward': 0} 		|	 18.51
 	{'price': 1, 'reward': 0.25} 	|	 180.0675
 	{'price': 1, 'reward': 0.5} 	|	 60.675
'''

''' (delta=0.2)
{'reward': 0, 'price': 1} 		|	 229.66
{'reward': 0.25, 'price': 1} 	|	 309.8125
{'reward': 0.5, 'price': 1} 	|	 72.105
'''


''' 9 possible actions
{'reward': 0, 'price': 0.9}     |        165.7620000000006
{'reward': 0.25, 'price': 0.9}  |        166.01050000000055
{'reward': 0.5, 'price': 0.9}   |        282.8619999999992
{'reward': 0, 'price': 1}       |        151.87
{'reward': 0.25, 'price': 1}    |        154.1025
{'reward': 0.5, 'price': 1}     |        256.92
{'reward': 0, 'price': 1.1}     |        135.56399999999962
{'reward': 0.25, 'price': 1.1}  |        135.63699999999963
{'reward': 0.5, 'price': 1.1}   |        219.41999999999945
'''
