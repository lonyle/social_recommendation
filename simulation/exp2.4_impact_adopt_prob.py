import json
import firm
import setting
import numpy as np

attention = 1
trust = 1 # when gamma=1, the trust has no impacts
eta = 0.5

BASELINE_PRICE = 1

def impact_initial_adopt_prob():
	'''
	the initial recommendation probability under state FriRec
	'''
	tmp_filename = 'data/result_initial_adopt_prob_profit.json'
	results = dict()

	firm_param = setting.baseline_firm_param

	adopt_prob_vec = list(np.linspace(0.04, 0.4, 10))
	results['adopt_prob_vec'] = adopt_prob_vec
	results['strategy_vec'] = []
		
	for adopt_prob in adopt_prob_vec:
		firm_param['adopt_prob_type'] = {'zero': adopt_prob, 'small': adopt_prob, 'large': adopt_prob}
		one_firm = firm.Firm(firm_param)

		one_firm.opt_strategy(attention, trust, eta)

		############################
		# calculating the social value		
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
	impact_initial_adopt_prob()