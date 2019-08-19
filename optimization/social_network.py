# edited on 2019-1-5: we do not choose a random user from the candidates, nor do we choose from queue
# we choose an arbitrary item from a set ( set.pop() )
#import queue

import random
import math
import hashlib
import argparse
#import mcts

import facebook_osn
import yelp_osn
import utils


# record the global state of the depth-first search, the state reports whether each user adopt the item
#global_graph = None

class Graph():
	''' the graph that is used to find the optimal policy for given parameters
	'''
	def __init__(self, delta, rec_prob_func, adopt_prob_func):
		print ('constructing the simulator over a graph')
		if utils.graph_name == 'Facebook':
			self.edges = facebook_osn.get_edges() # load the graph
		elif utils.graph_name == 'Yelp':
			self.edges = yelp_osn.get_edges() # load the Yelp graph
		else:
			print ('wrong graph name !!!!')
			
		self.nodes = self.edges.keys()
		self.N_user = len(self.edges)
		self.N_other_info = int(self.N_user * delta)
		
		self.delta = delta
		self.rec_prob_func = rec_prob_func
		self.adopt_prob_func = adopt_prob_func

		self.feedbacks = dict() # whether adopt and whether recommend
		self.reset()

	def reset(self):
		# print ('resetting the graph')
		self.is_recommended = dict()
		for node in self.nodes:
			self.is_recommended[node] = False

		self.N_is_recommended = 0
		# randomly choose int(N_users * delta) in the later_other_info
		
		random_other_info = list(random.sample(self.nodes, self.N_other_info))
		self.already_other_info_set = set()
		# edited on 2019-1-5: return a shuffled list
		self.later_other_info_set = set(random_other_info)
		random.shuffle(random_other_info) 
		self.later_other_info = random_other_info[:]# the users who will be informed by others, randomly assigned at beginning
		self.newly_recommended_set = set() # now, but to a set
		self.cost_on_reward = 0
		self.gross_profit = 0
		self.n = 0 # initially, no user is informed from other information

	def next(self, action):
		''' be compatible with the old version of 'next' function
		'''
		# selected_user = self.node_arrival()
		selected_user = self.node_arrival_weighted() # edited on 2019-01-16, use the weighted version
		transition_profit = self.do_action(selected_user, action)
		return transition_profit

	def node_arrival_weighted(self):
		''' the picked user could be in the newly_recommended_set or later_other_info_set with certain probability
		'''
		N_newly_recommended = len(self.newly_recommended_set)
		N_later_other_info = len(self.later_other_info)

		if N_newly_recommended + N_later_other_info == 0:
			return None # no more users will arrive

		weight_newly_recommended = 1
		weight_later_other_info = 1

		# the prob. that some user is selected who is informed of other information
		p_later_other_info = (N_later_other_info * weight_later_other_info) / (N_later_other_info * weight_later_other_info + N_newly_recommended * weight_newly_recommended)
		if random.random() < p_later_other_info: # select one from other_info
			while True:
				if len(self.later_other_info) > 0:
					selected_user = self.later_other_info.pop()
				else:
					return None
				if self.is_recommended[selected_user] == False:
					break
			self.n += 1
			self.already_other_info_set.add(selected_user)
			self.later_other_info_set.remove(selected_user)
		else: # select one from newly_recommended
			selected_user = self.newly_recommended_set.pop()
			#self.is_recommended[selected_user] = True
			self.N_is_recommended += 1
			if selected_user in self.already_other_info_set:
				return None
		return selected_user

	def node_arrival(self):
		''' randomly pick a user in the newly_recommended_set, or in later_other_info_set
			this is the old version, and picks a node from newly_recommended_set first
		'''
		#print ('calling the next function, action:', action)

		if len(self.newly_recommended_set) == 0: # if no user is newly recommended
			if len(self.later_other_info) > 0:
				# let one of the users in later_other_info to be informed
				while True: # wait until the first user who is not informed from other information
					if len(self.later_other_info) > 0:
						selected_user = self.later_other_info.pop()
					else: # if no more user in the later_other_info, return None
						return None
					if self.is_recommended[selected_user] == False: # only for the users who have not receive recommendations
						break
				self.n += 1
				self.already_other_info_set.add(selected_user)
				self.later_other_info_set.remove(selected_user)
				
			else: # no user will be informed by any information sources
				return None # no next state, skip the processing for selected_user
		else: # if some selected user is newly recommended
			selected_user = self.newly_recommended_set.pop()
			
			#self.is_recommended[selected_user] = True
			self.N_is_recommended += 1

			if selected_user in self.already_other_info_set:
				return None # do nothing, already been informed by other information
				#this is because we assume that the rec_prob and adopt_prob are the same for users informed from different sources
		return selected_user

	def do_action(self, selected_user, action):
		'''	then decide the users' action according to the sales strategy (action) of the firm
			the action of the chosen user decide the next state
			return: the immediate reward. We also record the changed state
		'''
		self.feedbacks = {'adopt': None, 'recommend': None}
		transition_profit = 0 # the profit gain by transiting from the current state to the next state
		if selected_user == None: # if no more user will arrive, the profit is 0
			return 0

		# currently, the users informed from other_info or from recommendations have the same prob.
		adopt_prob = self.adopt_prob_func(action['price'], action['reward'])
		rec_prob = self.rec_prob_func(action['price'], action['reward'])
		adopt_prob = min(1, adopt_prob)
		rec_prob = min(1, rec_prob)

		transition_profit += adopt_prob * action['price']
		transition_profit -= rec_prob * action['reward']

		if random.random() < adopt_prob:
			self.gross_profit += action['price'] # representing price-cost		
			self.feedbacks['adopt'] = True
		else:
			self.feedbacks['adopt'] = False
			
		# assume only the adopter will recommend
		if random.random() < rec_prob: # this fomula assume recommendation and adoption are independent, which is ok as only recommendation matters for disffusion
			# the spending on the reward 
			self.cost_on_reward += action['reward']
			self.feedbacks['recommend'] = True
			# the friends of this user will receive recommendation
			for friend in self.edges[selected_user]:
				## for Yelp, some friend may not be in the social network? For such cases, continue
				if friend not in self.is_recommended: # skip this one
					continue
				if self.is_recommended[friend] == False: # newly recommended
					self.newly_recommended_set.add(friend)
					self.is_recommended[friend] = True
				if friend in self.later_other_info_set: # someone will not receive other info
					self.later_other_info_set.remove(friend)
		else:
			self.feedbacks['recommend'] = False

		return transition_profit



	def current_state_param(self): # return the state needed by MCTS
		m = self.N_is_recommended # optimize, directly return the number of recommended
		delta_m = len(self.newly_recommended_set)
		delta_n = len(self.later_other_info_set) # who will be informed from other information
		n = self.n
		#if m % 1000 == 0:
		#print ('current_state_param: m=%d, delta_m=%d, n=%d, delta_n=%d'%(m, delta_m, n, delta_n) )
		return m, delta_m, n, delta_n


	# more used by thompson_sampling
	def get_feedbacks(self):
		# know whether adopt or recommend
		return self.feedbacks

	def is_terminated(self):
		m, delta_m, n, delta_n = self.current_state_param()
		if delta_m + delta_n == 0:
			return True
		return False






