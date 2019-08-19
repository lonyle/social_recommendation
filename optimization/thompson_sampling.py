import numpy as np
import social_network
import q_learning
import q_learning_big_transition
import logging
import utils
import time_variant_mixed
import opt_mixed
import influence_cutoff

# do not know the parameters (delta, action-to-prob table)
''' record the number of success and failure, and the posterior comes with beta distribution
'''

possible_actions = utils.possible_actions
action_to_idx_dict = dict()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('thompson-sampling')

def init():
	for idx in range(len(possible_actions)):
		action = possible_actions[idx]
		action_key = utils.action_to_key(action)
		action_to_idx_dict[action_key] = idx


EPOCH_SIZE = 100

# class Simulator(social_network.Graph):
# 	''' do the simulation on the social network graph with the ground-truth parameter
# 	'''
# 	def __init__(self, delta, rec_prob_func, adopt_prob_func):
# 		print('constructing the simulator!')
# 		super(Simulator, self).__init__(delta, rec_prob_func, adopt_prob_func)

# 	def get_feedbacks(self):
# 		# know whether adopt or recommend
# 		return self.feedbacks

# 	def is_terminated(self):
# 		m, delta_m, n, delta_n = self.current_state_param()
# 		if delta_m + delta_n == 0:
# 			return True
# 		return False


class PSRL():
	''' do the posterior sampling and learning at the same time
	'''
	def __init__(self, default_success=1, default_failure=1):
		self.n_arms = len(possible_actions)
		self.prior_success = dict()
		self.prior_failure = dict()
		# two kinds of behaviors of users
		for behavior in ['adopt', 'recommend']:
			self.prior_success[behavior] = np.array([default_success for arm in range(self.n_arms)])
			self.prior_failure[behavior] = np.array([default_failure for arm in range(self.n_arms)])

	def action_to_idx(self, action):
		''' from the action dictionary to the arm-index
		'''
		action_key = utils.action_to_key(action)
		return action_to_idx_dict[action_key]


	def get_param_posterior_sample(self):
		posterior_sample = dict()
		for behavior in ['adopt', 'recommend']:
			posterior_sample[behavior] = np.random.beta(self.prior_success[behavior], self.prior_failure[behavior])
		
		return posterior_sample

	def update_observation(self, action, feedbacks):
		for behavior in ['adopt', 'recommend']:
			if feedbacks[behavior] == True:
				self.prior_success[behavior][self.action_to_idx(action)] += 1
			elif feedbacks[behavior] == False:
				self.prior_failure[behavior][self.action_to_idx(action)] += 1

	def pick_decision_func(self, delta, num_sims, method_name):
		''' return a decision function: state -> action
		'''
		param_posterior_sample = self.get_param_posterior_sample()
		# convert the int-indexed parameters to key-indexed parameters
		param_dict = dict()
		for behavior in ['adopt', 'recommend']:
			param_dict[behavior] = dict()
			for i in range(len(possible_actions)):
				action = possible_actions[i]
				action_key = utils.action_to_key(action)
				param_dict[behavior][action_key] = param_posterior_sample[behavior][i]

		if method_name == 'q-learning':
			decision_func = q_learning_big_transition.find_decision_func(num_sims, delta, param_dict)
		elif method_name == 'mixed':
			decision_func = opt_mixed.find_decision_func(num_sims, delta, param_dict)
		elif method_name == 'influence':
			decision_func = influence_cutoff.find_decision_func(num_sims, delta, param_dict)
		else:
			logger.warning('wrong method_name!!')

		return decision_func

def runner(true_delta, true_rec_prob_func, true_adopt_prob_func, method_name='q-learning'):
	is_node_feature = True if method_name == 'influence' else False
	if method_name == 'influence':
		influence_cutoff.ROUND_PEDGE = True

	init()
	simulator = social_network.Graph(true_delta, true_rec_prob_func, true_adopt_prob_func)
	psrl = PSRL()
	epoch_count = 0
	while simulator.is_terminated() == False:
		epoch_count += 1
		logger.info('choosing new decision function in epoch %d ...'%(epoch_count))

		num_sims = int(epoch_count ** 1.5) * 2 # number of simulation should not be very large, or otherwise, the running time is high
		decision_func = psrl.pick_decision_func(true_delta, num_sims, method_name) # now, we use the true delta

		epoch_size = int(epoch_count ** 1.5)
		for i in range(epoch_size):
			logger.info('epoch %d, iteration %d'%(epoch_count, i))

			## copied from evaluate.py on 2019-01-25
			selected_user = simulator.node_arrival()
			degree = len(simulator.edges[selected_user]) if selected_user != None else None
			node_feature = {'degree': degree, 'id': selected_user}
			current_state_param = simulator.current_state_param()
			if is_node_feature: # enable the firm to use node feature
				action = decision_func(current_state_param, node_feature)
			else:
				action = decision_func(current_state_param)
			simulator.do_action(selected_user, action)

			######### the old version:
			# state_param = simulator.current_state_param()
			# action = decision_func(state_param)
			# simulator.next(action)
			############################

			feedbacks = simulator.get_feedbacks()

			psrl.update_observation(action, feedbacks)

	profit = simulator.gross_profit - simulator.cost_on_reward
	return profit

if __name__ == '__main__':
	#### the ground truth ####
	true_delta = 0.2#0.01 # currently, do not need to estimate
	def true_rec_prob_func(price, reward):
		rec_prob = 0.02 + 0.3 * reward
		return rec_prob
	def true_adopt_prob_func(price, reward):
		adopt_prob = 0.1 + 0.2 * (1-price)
		return adopt_prob
	##########################

	profit = runner(true_delta, utils.true_rec_prob_func, utils.true_adopt_prob_func, \
		'influence')
	print ('the one-shot profit from our algorithm is:', profit)
	# the one-shot profit from our algorithm is: 183.0