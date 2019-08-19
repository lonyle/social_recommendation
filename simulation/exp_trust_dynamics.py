# firms will decide the opt strategy according to the trust of 
# firms' strategies affects customers' trust

import firm
import json
import numpy as np 
import setting

valuation = 1
attention = 1

output_filename = 'data/result_trust_dynamics.json'

def opt_single_firm():
	limit_recommendation = np.inf
	firm_param = setting.baseline_firm_param
	one_firm = firm.Firm(firm_param)
	####################
	# !!!!!!! important 
	one_firm.gamma = 0.5 # chagne the gamma value
	####################

	price_vec = np.linspace(0.001, 2, firm.N_GRID)#[self.old_price]	
	reward_vec = np.linspace(0, 2, firm.N_GRID)	
	opt_profit = -np.inf
	for price in price_vec:
		for reward in reward_vec:
			_profit = one_firm.get_long_term_profit(price, reward, limit_recommendation)
			if _profit > opt_profit:
				opt_profit = _profit
				opt_price = price
				opt_reward = reward

			print (price, reward, _profit)

	print ('opt_profit:', opt_profit)
	print ('opt_price:', opt_price)
	print ('opt_reward:', opt_reward)

def trust_dynamics(N_iteration, N_firms):
	firm_param = setting.baseline_firm_param
	firms = []
	utility_ratio_vec = [] # the utility ratio for the firms
	for n in range(N_firms):
		one_firm = firm.Firm(firm_param)
		####################
		# !!!!!!! important 
		one_firm.gamma = 0.5 # chagne the gamma value
		####################
		firms.append(one_firm)
		utility_ratio_vec.append(valuation/one_firm.opt_price)
	
	# initialize the trust
	trust = sum(utility_ratio_vec)/N_firms

	# dynamics of the trust	
	reward_vec = []
	price_vec = []
	profit_vec = []
	trust_vec = []
	for ite in range(N_iteration):
		print ('#### iteration:', ite)
		i = np.random.randint(len(firms)) # randomly pick a firm
		one_firm = firms[i]
		print ('# firm', i)

		one_firm.opt_strategy(attention, trust)
		print ('reward:', one_firm.opt_reward, 'profit:', one_firm.opt_profit)
		reward_vec.append(one_firm.opt_reward)
		profit_vec.append(one_firm.opt_profit)
		price_vec.append(one_firm.opt_price)

		#### update the trust			
		utility_ratio_vec[i] = valuation / one_firm.opt_price
		trust = sum(utility_ratio_vec)/N_firms
		trust_vec.append(trust)
		print ('trust:', trust)

	with open(output_filename, 'w') as output_file:
		json.dump({'reward_vec': reward_vec, 'profit_vec': profit_vec, \
			'trust_vec': trust_vec, 'price_vec': price_vec}, output_file, indent=4)

if __name__ == '__main__':
	N_iteration = 50
	N_firms = 10
	trust_dynamics(N_iteration, N_firms)
	
	#opt_single_firm()
	''' result
	opt_profit: 101210.2828272783
	opt_price: 1.26703333333
	opt_reward: 0.666666666667
	'''