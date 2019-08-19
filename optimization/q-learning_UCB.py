# created on 12-28: copied from q-learning.py
# modifition from q-learnig.py: use UCB strategy for exploration

import random
import math
import logging
import social_network
import evaluate
import facebook_osn
import argparse
import matplotlib.pyplot as plt
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('q-learning-improved')
LOG_STEP = 100

ALPHA = 0.1 # learning rate
SCALAR = 1/math.sqrt(2.0)
EPSILON_SCALAR = 0.01 # the minimum value of epsilon value is EPSILON_SCALAR/sqrt(num_sims)

state_dict = dict() # store the information of the state table

# possible_reward = [0.0, 0.1, 0.2, 0.3]# action space
# possible_price = [0.9, 1.0, 1.1]# action space
possible_reward = [0, 0.5]
possible_price = [1]
possible_actions = []
for reward in possible_reward:
	for price in possible_price:
		possible_actions.append({'reward': reward, 'price': price})


def state_param_to_key(state_param):
	m, delta_m, n, delta_n = state_param
	big_informed_index = (m+n) // 100 * 100
	return str(big_informed_index) + ',' + str(delta_m + delta_n)


class State():
	def __init__(self, state_key, is_terminal=False):
		self.state_key = state_key
		self.is_terminal = is_terminal
		
		self.visits = 0

		self.unexplored_actions = possible_actions[:]

		self.action_dict = dict()
		for action in possible_actions:
			key = utils.action_to_key(action)
			self.action_dict[key] = {'count': 0, 'q': 0, 'sum_q': 0} # prepared to calculate the average


		self.max_actions = []

	def get_max_q(self):
		# bug here, if q value is updated, we should use the latest q-value
		if self.is_terminal == True:
			return 0 # 0 q-value for the terminal nodes

		max_q = 0
		self.max_actions = []
		for action in possible_actions:
			action_key = utils.action_to_key(action)
			if self.action_dict[action_key]['q'] == max_q:
				self.max_actions.append(action)
			elif self.action_dict[action_key]['q'] > max_q:
				max_q = self.action_dict[action_key]['q']
				self.max_actions = [action]

		return max_q

	def update_q_value(self, action, new_value): # new value equals r+next_state.max_q
		action_key = utils.action_to_key(action)

		# update the q-value
		if self.action_dict[action_key]['count'] == 0:
			q = new_value # if new previous record, use the latest value
		else:
			old_q = self.action_dict[action_key]['q']
			# print('old_q:', old_q, 'r:', r, 'next_state.max_q:', next_state.get_max_q() )
			q = (1-ALPHA)*old_q + ALPHA*( new_value )

		self.action_dict[action_key]['q'] = q
		self.action_dict[action_key]['sum_q'] += new_value
		# wait until updating the 'count' value to mark it explored
		if self.action_dict[action_key]['count'] == 0:
			self.unexplored_actions.remove(action)
		self.action_dict[action_key]['count'] += 1

	def get_q_value(self, action):
		action_key = utils.action_to_key(action)
		return self.action_dict[action_key]['q']


	def best_action(self, scalar): # UCB-style, following the paper
		#print (self.unexplored_actions)
		if len(self.unexplored_actions) > 0:
			choice = random.choice(self.unexplored_actions)
			return choice
		
		# find the max. average, do normalization
		MAX_AVERAGE = 0
		for action in possible_actions:
			action_key = utils.action_to_key(action)
			exploit = self.action_dict[action_key]['sum_q'] / self.action_dict[action_key]['count']
			if exploit > MAX_AVERAGE:
				MAX_AVERAGE = exploit

		bestscore = 0
		bestactions = []
		for action in possible_actions:
			action_key = utils.action_to_key(action)
			exploit = self.action_dict[action_key]['sum_q'] / self.action_dict[action_key]['count'] 
			explore = math.sqrt(2.0*math.log(self.visits)/float(self.action_dict[action_key]['count']))
			score = exploit / MAX_AVERAGE + scalar * explore
			if score == bestscore:
				bestactions.append(action)
			if score > bestscore:
				bestactions = [action]
				bestscore = score

		if len(bestactions) == 0:
			logger.warning('the max_action vector is empty')
			return random.choice(bestactions)
		return random.choice(bestactions)

	def __repr__(self):
		return 'State: %s \t visits:%d'%(self.state_key, self.visits)



def forward_simulation(graph, root_state, root_param, n, is_log = False):
	''' do forward_simulation, and update the q-function
	'''
	graph.reset()

	state_seq = []  # including the terminating state
	action_seq = [] # 
	r_seq = []

	current_state = root_state
	while current_state.is_terminal == False:
		if is_log:
			logger.info(current_state)
		
		current_state.visits += 1
		epsilon = math.sqrt( 1/(n+1) ) # devided by the number of iterations, i.e. n
		action = current_state.best_action(SCALAR)

		r = graph.next(action)

		### recording the results ###
		state_seq.append(current_state)
		action_seq.append(action)
		r_seq.append(r)
		#############################

		next_state_param = graph.current_state_param()

		next_state_key = state_param_to_key(next_state_param)

		# if encountering a new state
		if next_state_key not in state_dict:
			is_terminal = (next_state_param[1] + next_state_param[3] == 0)
			state_dict[next_state_key] = State(next_state_key, is_terminal)

		next_state = state_dict[next_state_key]

		current_state = next_state

	state_seq.append(current_state)

	return state_seq, action_seq, r_seq

def backward_update(state_seq, action_seq, r_seq, is_log):
	''' starting from the last visited state, go back and do the update
	'''
	n_state = len(state_seq)
	for i in range(n_state-2, -1, -1):
		next_state = state_seq[i+1]
		current_state = state_seq[i]

		action = action_seq[i]
		r = r_seq[i]


		######### print the q-value before and after updating along the path #########
		if is_log:
			print ('current state:', current_state)
			print ('action:', action)
			print ('q-value before updating:', current_state.get_q_value(action) )

		new_value = r+next_state.get_max_q()
		current_state.update_q_value( action, new_value )

		if is_log:
			print ('new_value:', new_value, 'updated_value:', current_state.get_q_value(action) )

	return 0

def update_q_table(num_sims, graph):
	# initialize the root
	root_key = '0,'+str(graph.N_other_info)
	root_state = State(root_key)
	state_dict[root_key] = root_state

	for n in range(num_sims):
		if n % LOG_STEP == 0:
			is_log = True
		else:
			is_log = False

		logger.info('number of simulation:%d', n)
		state_seq, action_seq, r_seq = forward_simulation(graph, root_state, n, is_log)
		backward_update(state_seq, action_seq, r_seq, is_log)

		if n % LOG_STEP == 0:
			price_seq = [action['price'] for action in action_seq]
			reward_seq = [action['reward'] for action in action_seq]
			# plt.plot(price_seq, color='blue')
			# plt.plot(reward_seq, color='red')
			# plt.show()

def decision_func(state_param):
	key = state_param_to_key(state_param)
	if key in state_dict:		
		action = state_dict[key].best_action(0)
		return action
	else: # not in the state_dict (not visited), return a random action
		logger.warning('state not visited: %s', key)
		print (state_param)
		return random.choice(possible_actions)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'q-learning')
	parser.add_argument('--num_sims', action = 'store', required = True, type = int, \
		help = 'Number of simulations to run')
	args = parser.parse_args()

	num_sims = args.num_sims

	delta = 0.01

	# def rec_prob_func(price, reward):
	# 	rec_prob = 0.1 + 0.2 * reward 
	# 	return rec_prob

	# def adopt_prob_func(price, reward):
	# 	adopt_prob = 0.1 + 0.1 * (1-price)
	# 	return adopt_prob

	def rec_prob_func(price, reward):
		rec_prob = 0.02 + 0.3 * reward
		return rec_prob

	def adopt_prob_func(price, reward):
		adopt_prob = 0.1 + 0.2 * (1-price)
		return adopt_prob

	graph = social_network.Graph(delta, rec_prob_func, adopt_prob_func)

	update_q_table(num_sims, graph)

	# evaluating the learned decisions
	average = evaluate.evaluate_average(graph, decision_func, 100)
	print ('average profit of the learned decision policy:', average)

















