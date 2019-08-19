# Exp 5: the impact of perceivability (and trust)

# change the parameter "gamma" for the firm, and "trust" of the environment
# see the impact on profit, opt_price, opt_reward

import json
import setting
import numpy as np
import firm

attention = 1

trust = 0 # here, we also need to change the trust!! [0.5, 1, 2]
eta = 0.5

BASELINE_PRICE = 1

# def perceivability_profit():
# 	tmp_filename = 'data/result_perceivability_trust'+str(trust)+'.json'
# 	results = dict()

# 	firm_param = setting.baseline_firm_param

# 	gamma_vec = np.linspace(0, 1, 15) # the param for perceivability

# 	reward_vec = [0, 0.1, 0.2]
# 	profit_vec = []

# 	for reward in reward_vec:
# 		for gamma in gamma_vec:
# 			firm_param['gamma'] = gamma 
# 			one_firm = firm.Firm(firm_param)
# 			profit = one_firm.get_profit(price, reward, attention, trust)
# 			profit_vec.append(profit)
# 		results[reward] = {'gamma_vec': gamma_vec, 'profit_vec': profit_vec}

# 	with open(tmp_filename, 'w') as output_file:
# 		json.dump(results, output_file, indent=4)


def perceivability_opt_strategy():
	tmp_filename = 'data/result_perceivability_opt_strategy'+str(trust)+'.json'
	results = dict()

	firm_param = setting.baseline_firm_param

	gamma_vec = list( np.linspace(0.5, 1, 15) ) # the param for perceivability


	results['gamma_vec'] = gamma_vec

	results['strategy_vec'] = []
	for gamma in gamma_vec:
		firm_param['gamma'] = gamma 
		one_firm = firm.Firm(firm_param)
		one_firm.opt_strategy(attention, trust, eta)

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
		 	'average_price': average_price,
		 	'baseline_profit': baseline_profit,
		 	'baseline_price': baseline_price,
		 	'baseline_social_value': baseline_social_value
		 }

		results['strategy_vec'].append(result)

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

if __name__ == '__main__':
	perceivability_opt_strategy()