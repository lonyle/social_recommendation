import json
import firm
import setting
import numpy as np

attention = 1
trust = 1 # when gamma=1, the trust has no impacts
eta = 0.5

BASELINE_PRICE = 1

def impact_initial_rec_prob():
	'''
	the initial recommendation probability under state FriRec
	'''
	tmp_filename = 'data/result_initial_rec_prob_profit.json'
	results = dict()

	firm_param = setting.baseline_firm_param

	rec_prob_vec = [0.001, 0.005] + list(np.linspace(0.01, 0.15, 13))
	# list(np.linspace(0.001, 0.02, 5)) + list(np.linspace(0.02, 0.1, 10))
	results['rec_prob_vec'] = rec_prob_vec
	results['strategy_vec'] = []
		
	for rec_prob in rec_prob_vec:
		small_prob = rec_prob 
		large_prob = rec_prob * setting.occupation_scale['large']/setting.occupation_scale['small']
		firm_param['rec_prob_FriRec_type'] = {'zero': 0, 'small': small_prob, 'large': large_prob}
		# firm_param['adopt_prob_type'] = {'zero': 0, 'small': small_prob, 'large': large_prob}
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
		 	'baseline_profit': baseline_profit,
		 	'baseline_price': baseline_price,
		 	'baseline_social_value': baseline_social_value,
		 	'average_price': average_price
		 }
		 
		results['strategy_vec'].append(result)

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

if __name__ == '__main__':
	impact_initial_rec_prob()
