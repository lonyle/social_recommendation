# two kinds of interactions: customers' attentions, customers' trust
# what is the dynamics and equilibrium of firms' strategies

import firm
import json
import numpy as np
import setting

output_filename = 'data/result_attention_dynamics.json'

trust = 1

LIMIT_SCALE = 2 # limit attention / current attention used

def opt_single_firm(limit_recommendations):
	firm_param = setting.baseline_firm_param
	one_firm = firm.Firm(firm_param)

	price_vec = np.linspace(0.01, 3, firm.N_GRID)#[self.old_price]	
	reward_vec = np.linspace(0, 3, firm.N_GRID)	
	opt_profit = -np.inf
	for price in price_vec:
		for reward in reward_vec:
			_profit = one_firm.get_long_term_profit(price, reward, limit_recommendations)
			if _profit > opt_profit:
				opt_profit = _profit
				opt_price = price
				opt_reward = reward

			print (price, reward, _profit)

	print ('opt_profit:', opt_profit)
	print ('opt_price:', opt_price)
	print ('opt_reward:', opt_reward)

def competing_attention(N_iteration, N_firms):
	# 10 firms, each firm has the same parameters

	firm_param = setting.baseline_firm_param

	firms = []
	N_recommendation_firms = []
	for n in range(N_firms):
		firms.append(firm.Firm(firm_param))

	
	attention = 1 # this initial value is important

	for one_firm in firms:
		N_recommendation = one_firm.get_N_recommendation\
			(one_firm.old_price, one_firm.old_reward, attention, trust)
		print ('N_recommendation:', N_recommendation)
		N_recommendation_firms.append(N_recommendation)

	sum_baseline_recommendations = sum(N_recommendation_firms)
	# use the current number of recommendations * LIMIT_SCALE as a limit
	limit_recommendations = sum_baseline_recommendations * LIMIT_SCALE	
	
	reward_vec = []
	price_vec = []
	profit_vec = []
	attention_scale_vec = []
	for ite in range(N_iteration):
		print ('#### iteration:', ite)
		i = np.random.randint(len(firms)) # randomly pick a firm
		one_firm = firms[i]
		print ('# firm id:', i)
		one_firm.opt_strategy(attention, trust)
		print ('reward:', one_firm.opt_reward, 'profit:', one_firm.opt_profit)
		reward_vec.append(one_firm.opt_reward)
		profit_vec.append(one_firm.opt_profit)
		price_vec.append(one_firm.opt_price)

		#### update the attention
		N_recommendation = one_firm.get_N_recommendation\
			(one_firm.opt_price, one_firm.opt_reward, attention, trust)
		N_recommendation_firms[i] = N_recommendation
		sum_recommendations = sum(N_recommendation_firms)
		
		attention = min(1, limit_recommendations/sum_recommendations)
		print ('attention_scale:', attention)
		attention_scale_vec.append(attention)

	with open(output_filename, 'w') as output_file:
		json.dump({'reward_vec': reward_vec, 'profit_vec': profit_vec, \
			'attention_scale_vec': attention_scale_vec, 'price_vec': price_vec}, output_file)


if __name__ == '__main__':
	# N_iteration = 50
	# N_firms = 10
	# competing_attention(N_iteration, N_firms)

	limit_recommendations = 2382
	opt_single_firm(limit_recommendations)
	'''
	opt_profit: 16275.6249153
	opt_price: 1.29142857143
	opt_reward: 0.244897959184
	'''
