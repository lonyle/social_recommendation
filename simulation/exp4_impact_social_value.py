# Exp 4: social value is directly added to the reward

# feed the reward to the firm, and set the scaling factor to get the actual reward spent

import json
import setting
import numpy as np
import firm

attention = 1
trust = 1 # when gamma=1, the trust has no impacts
eta = 0.5

BASELINE_PRICE = 1

# def social_value_profit():
# 	tmp_filename = 'data/result_social_value_profit.json'
# 	results = dict()

# 	firm_param = setting.baseline_firm_param

# 	one_firm = firm.Firm(firm_param)

# 	# eta is the param that controls the scale of social value
# 	#effective_reward = reward + eta * (price - 0.5) is the reward to improve rec. prob.
# 	eta_vec = list(np.arange(0, 4, 11))
# 	for eta in eta_vec:
# 		profit_vec = []
# 		for reward in reward_vec:
# 			effective_reward = reward + eta * (price - BASELINE_PRICE)
# 			setting.actual_reward_scale = reward / effective_reward
# 			profit = one_firm.get_profit(price, effective_reward, attention, trust)
# 			profit_vec.append(profit)

# 		results[eta] = profit_vec

# 	with open(tmp_filename, 'w') as output_file:
# 		json.dump(results, output_file, indent=4)

def social_value_opt_strategy():
	tmp_filename = 'data/result_social_value_opt_strategy.json'
	results = dict()

	firm_param = setting.baseline_firm_param
	one_firm = firm.Firm(firm_param)

	eta_vec = list(np.linspace(0, 2, 16))

	results['eta_vec'] = eta_vec
	results['strategy_vec'] = []
	for eta in eta_vec:
		print ('eta:', eta)
		one_firm.opt_strategy(attention, trust, eta) 

		############################
		# calculating the social value		
		unit_social_value = eta * (BASELINE_PRICE - one_firm.opt_price)
		effective_reward = one_firm.opt_reward + eta * (BASELINE_PRICE - one_firm.opt_price)
		N_recommendation = one_firm.get_N_recommendation(\
			one_firm.opt_price, one_firm.opt_reward, attention, trust, effective_reward)
		social_value = unit_social_value * N_recommendation
		############################

		############################
		# average price
		average_price = one_firm.get_average_price(one_firm.opt_price, one_firm.opt_reward, attention, trust)
		############################

		############################
		# getting the baseline profit
		baseline_profit, baseline_price, baseline_social_value = one_firm.get_baseline(attention, trust, eta)
		############################

		result = {
			'opt_price': one_firm.opt_price, 
			'opt_profit': one_firm.opt_profit, 
			'opt_reward': one_firm.opt_reward,
		 	'social_value': social_value,
		 	'baseline_profit': baseline_profit,
		 	'baseline_price': baseline_price,
		 	'baseline_social_value': baseline_social_value,
		 	'average_price': average_price
		 }

		results['strategy_vec'].append(result)

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

if __name__ == '__main__':
	#social_value_profit()
	social_value_opt_strategy()


