import profit
import numpy as np
import setting
import json

import sys
sys.path.insert(0, 'inference')

import infer_behavior

N_GRID = setting.N_GRID

BASELINE_PRICE = 1


'''
the parameters of a firm. For example,
firm_param = {
	'other_info_prob': 0.01, # consider the scaling for state OthInf
	'rec_prob_FriRec_type': {'small': xxx, 'medium': xxx, 'large': xxx},
	'adopt_prob_type': {'small': xxx, 'medium': xxx, 'large': xxx}, # no difference between different types
	'gamma': 0.5, # a number in [0,1]
	'cost': 0,
	'old_reward': 0,
	'old_price': 1
}
'''
class Firm: # behave like a firm
	def __init__(self, firm_param):
		# attributes (current)
		self.other_info_prob = firm_param['other_info_prob']
		self.old_rec_prob_FriRec_type = firm_param['rec_prob_FriRec_type'] # in our model, the rec_prob_OthInf is proportional to rec_prob_FriRec
		self.old_rec_prob_OthInf_type = self.old_rec_prob_FriRec_type
		self.adoption_prob_type = firm_param['adopt_prob_type']
		self.gamma = firm_param['gamma']
		#self.stars = firm['stars'] # TODO: later add the dimension stars
		self.cost = firm_param['cost']

		# related to the strategy
		self.old_reward = firm_param['old_reward']
		self.old_price = firm_param['old_price']

		# as the initialization
		self.opt_reward = self.old_reward
		self.opt_price = self.old_price

	# infer the rec. prob. based on the current price and reward
	# !!!! return two params: 
	def get_rec_prob(self, price, reward, trust):
		# map the change of trust to the chagne of price
		#delta_p = -(1-self.gamma) * (trust-setting.old_trust) * price / (self.gamma)# + trust)
		
		# now, map the change of perceivability to the change of price
		#delta_p = -(1-self.gamma) * price * trust
		delta_p = (1-self.gamma) * (1-price*(trust+1))
		effective_price_FriRec = price + delta_p
		effective_price_OthInf = price + (1-self.gamma) * (1-price*(-0.5+1))
		rec_prob_FriRec_type = infer_behavior.inf_rec_prob(effective_price_FriRec, reward, self.old_price, self.old_reward, self.old_rec_prob_FriRec_type)
		# for the users with OthInf, the trust = 0
		rec_prob_OthInf_type = infer_behavior.inf_rec_prob(effective_price_OthInf, reward, self.old_price, self.old_reward, self.old_rec_prob_OthInf_type)
		return rec_prob_FriRec_type, rec_prob_OthInf_type

	def get_adopt_prob(self, price, reward, trust):
		#delta_p = -(1-self.gamma) * (trust-setting.old_trust) * price / (self.gamma)# + trust)
		delta_p = (1-self.gamma) * (1-price*(trust+1))
		#delta_p = -(1-self.gamma) * price * trust
		effective_price_FriRec = price + delta_p
		effective_price_OthInf = price + (1-self.gamma) * (1-price*(-0.5+1))
		adopt_prob_FriRec_type = infer_behavior.inf_adopt_prob(effective_price_FriRec, reward, self.old_price, self.old_reward, self.adoption_prob_type)
		adopt_prob_OthInf_type = infer_behavior.inf_adopt_prob(effective_price_OthInf, reward, self.old_price, self.old_reward, self.adoption_prob_type)
		return adopt_prob_FriRec_type, adopt_prob_OthInf_type

	def get_N_recommendation(self, price, reward, attention, trust, effective_reward=None):
		_, N_recommendation, _ = self.get_profit_and_recommendation(price, reward, attention, trust, effective_reward)
		return N_recommendation

	def get_long_term_profit(self, price, reward, limit_recommendations, effective_reward=None):
		'''
		fix the price and reward, let the trust and attention evolve
		'''
		# init
		attention = 1
		valuation = 1
		trust = valuation / price
		N_iteration = 50

		attention_vec = []
		for i in range(N_iteration):
			_profit, N_recommendation = self.get_profit_and_recommendation(price, reward, attention, trust)
			if attention == 1 and N_recommendation <= limit_recommendations:
				break # if attention is always enough
			attention_vec.append( min(1,limit_recommendations / N_recommendation) )
			attention = sum(attention_vec) / len(attention_vec)
			#print ('iteration:', i, 'attention:', attention)

		return _profit


	def get_profit(self, price, reward, attention, trust, effective_reward=None):
		_profit, _, _ = self.get_profit_and_recommendation(price, reward, attention, trust, effective_reward)
		return _profit

	# attention: the $\alpha$ in the paper, scaling factor related to users' attention
	# trust: the $\tau$ in the paper, affecting user's estimated utility
	def get_profit_and_recommendation(self, price, reward, attention, trust, effective_reward=None):
		if effective_reward == None:
			effective_reward = reward
		rec_prob_FriRec_type, rec_prob_OthInf_type = self.get_rec_prob(price, effective_reward, trust)
		########### the following corresponds to two assumptions ############
		# 1. do not disdinguish prob. for OthInf and FriRec (since we don't know whether a user get other info.)
		# 2. extreme case adoption prob. does not change when price or reward changes
		# !!!!!! Here, we choose the case 2: does not change
		adopt_prob_FriRec_type, adopt_prob_OthInf_type = self.get_adopt_prob(price, reward, trust) 
		#adopt_prob_OthInf_type = adopt_prob_FriRec_type

		for Type in setting.Types:
			rec_prob_FriRec_type[Type] *= attention
			rec_prob_OthInf_type[Type] *= attention

			adopt_prob_FriRec_type[Type] *= attention
			adopt_prob_FriRec_type[Type] = max(adopt_prob_FriRec_type[Type], rec_prob_FriRec_type[Type]) # to avoid the case where inferred rec_prob is higher than inferred adopt_prob

			adopt_prob_OthInf_type[Type] *= attention
			adopt_prob_OthInf_type[Type] = max(adopt_prob_OthInf_type[Type], rec_prob_OthInf_type[Type])
				
		##########################################################
		_profit, N_recommendation, N_adoption = profit.get_estimated_profit(price, reward, self.cost, \
			self.other_info_prob, rec_prob_OthInf_type, rec_prob_FriRec_type,\
			 adopt_prob_OthInf_type, adopt_prob_FriRec_type)
		if isinstance(N_recommendation, float):
			return _profit, N_recommendation, N_adoption
		else:
			return np.asscalar(_profit), np.asscalar(N_recommendation), np.asscalar(N_adoption)

	def get_average_price(self, price, reward, attention, trust, effective_reward=None):
		''' this is the average price for the recommenders (p-r), and the adopters but non-recommenders (p)
		'''
		recommender_price = price - reward
		non_recommender_price = price
		_, N_recommendation, N_adoption = self.get_profit_and_recommendation(price, reward, attention, trust, effective_reward)
		print ('price:', price, 'reward:', reward)
		print ('N_recommendation:', N_recommendation, 'N_adoption:', N_adoption)
		average_price = recommender_price * N_recommendation + non_recommender_price * (N_adoption-N_recommendation)
		average_price /= N_adoption
		return average_price

	def get_baseline(self, attention, trust, eta=None): # the opt. profit without reward
		reward = 0
		opt_profit = -np.inf
		price_vec = np.linspace(0, 2, N_GRID)#[self.old_price]		
		for price in price_vec:
			if eta: # if social value is changed, add reward's effect
				effective_reward = reward + eta * (setting.BASELINE_PRICE - price)
				_profit = self.get_profit(price, reward, attention, trust, effective_reward)
			else:
				effective_reward = reward

			effective_reward *= setting.effective_reward_scale
			_profit = self.get_profit(price, reward, attention, trust, effective_reward)
			if _profit > opt_profit:
				opt_profit = _profit
				opt_price = price

		social_value = 0
		if eta:
			############################
			# calculating the social value		
			unit_social_value = eta * (BASELINE_PRICE - opt_price)
			effective_reward = reward + eta * (BASELINE_PRICE - opt_price)
			N_recommendation = self.get_N_recommendation(\
				opt_price, reward, attention, trust, effective_reward)
			social_value = unit_social_value * N_recommendation
			############################

		return opt_profit, opt_price, social_value

	def opt_strategy(self, attention, trust, eta=None):
		opt_reward = None
		opt_price = None
		opt_profit = -np.inf
		profit_vec = []
		price_vec = np.linspace(0, 2, N_GRID)#[self.old_price]		
		for price in price_vec:
			reward_vec = np.linspace(0, 2, N_GRID)
			for reward in reward_vec:
				if eta: # if social value is changed, add reward's effect
					effective_reward = reward + eta * (setting.BASELINE_PRICE - price)
				else:
					effective_reward = reward

				effective_reward *= setting.effective_reward_scale
				_profit = self.get_profit(price, reward, attention, trust, effective_reward)
				profit_vec.append(_profit)
				if _profit > opt_profit:
					opt_profit = _profit
					opt_price = price
					opt_reward = reward
		# print ('profit_vec:', profit_vec)
		# plt.axes([0.2, 0.15, 0.75, 0.75])
		# plt.plot(reward_vec, profit_vec, color='black')
		# plt.xlabel('reward $r$')
		# plt.ylabel('total net profit')
		# plt.savefig('images/opt_reward.eps', dpi=5000)
		# plt.show()
		self.opt_price = opt_price
		self.opt_reward = opt_reward
		self.opt_profit = opt_profit
		

if __name__ == '__main__':
	### prob. for a user to adopt the item
	# there are two extremes (1) the adoption prob. does not increase (2) the adoption prob. increase proportionally with the recommend prob
	# we first focus on the case (1)
	original_adoption_multiplier = 5 # adopt with prob. 5x of the prob. to recommend for type medium without reward

	firm_param = {
		'other_info_prob': 0.001, # consider the scaling for state OthInf
		'rec_prob_FriRec_type': {'zero': 0, 'small': 0.06, 'large': 0.03},
		'adopt_prob_type': {'zero': 0, 'small': 0.02, 'large': 0.01}, # no difference between different types
		'gamma': 1, # a number in [0,1]
		'cost': 0,
		'old_reward': 0,
		'old_price': 1
	}

	one_firm = Firm(firm_param)
	attention = 1
	trust = 0
	print (one_firm.baseline_profit(attention, trust))

	# 1st run: 0.02657155
