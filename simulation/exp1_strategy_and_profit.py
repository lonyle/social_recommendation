# Exp 1: the profit corresponding to different strategies of the firm
import firm

import numpy as np
import matplotlib.pyplot as plt
import json
import setting

attention = 1
trust = 0 # when gamma=1, the trust has no impacts

def reward_and_profit(one_firm):
	''' under different prices '''
	tmp_filename = 'data/result_reward_profit.json'

	price_vec = [0.8, 1, 1.2]
	reward_vec = list(np.linspace(0, 1, 15))
	results = dict()
	results['price_vec'] = price_vec
	results['reward_vec'] = reward_vec
	for price in price_vec:
		print ('##### the price is:', price)
		profit_vec = []
		for reward in reward_vec:
			print ('########## the reward is:', reward)
			profit = one_firm.get_profit(price, reward, attention, trust)
			print ('############### the profit is:', profit)
			profit_vec.append(profit)
		results[price] = profit_vec

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

def price_and_profit(one_firm):
	''' under different rewards '''
	tmp_filename = 'data/result_price_profit.json'

	reward_vec = [0]#, 0.2, 0.4]
	price_vec = list( np.linspace(0, 2, 41) )
	results = dict()
	results['price_vec'] = price_vec
	results['reward_vec'] = reward_vec
	for reward in reward_vec:
		profit_vec = []
		for price in price_vec:
			profit = one_firm.get_profit(price, reward, attention, trust)
			profit_vec.append(profit)
		results[reward] = profit_vec

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)


if __name__ == '__main__':
	firm_param = setting.baseline_firm_param
	one_firm = firm.Firm(firm_param)

	###########################
	# find the optimal pricing and rewarding strategy for the baseline
	# attention = 1
	# trust = 1
	# one_firm.opt_strategy(attention, trust)
	# print ('opt_price:', one_firm.opt_price)
	# print ('opt_profit:', one_firm.opt_profit)
	# print ('opt_reward:', one_firm.opt_reward)
	###########################

	reward_and_profit(one_firm)
	#price_and_profit(one_firm)


