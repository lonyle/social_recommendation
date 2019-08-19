# Exp 2: the impact of various factors revealed in the analysis on rewarding strategys
# x-axis is reward. Fix the price, or do small minor adjustment of price
import json
import firm
import setting
import numpy as np

attention = 1
trust = 0 # when gamma=1, the trust has no impacts

price = 1


def impact_effectiveness_reward():
	''' different enhancement by reward '''
	tmp_filename = 'data/result_effectiveness_reward_profit.json'

	firm_param = setting.baseline_firm_param

	one_firm = firm.Firm(firm_param)

	scale_vec = [0.01, 0.3, 1, 3]
	# the enhancement is 1/scale
	# the effective reward to improve rec. prob. is reward
	# the reward spent to recommenders is reward/scale

	reward_vec = list(np.linspace(0, 1, 11))

	results = dict()

	results['scale_vec'] = scale_vec

	for scale in scale_vec:
		
		profit_vec = []

		for reward in reward_vec:
			print ('########## the reward is:', reward)
			effective_reward = reward * scale
			profit = one_firm.get_profit(price, reward, attention, trust, effective_reward)
			print ('############### the profit is:', profit)
			profit_vec.append(profit)
		results[scale] = {'reward_vec': reward_vec, 'profit_vec': profit_vec}

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

#####################################
# the following changes parameters of the firm
#####################################

def impact_cost():
	''' change firm's cost, and get profit for different reward '''
	tmp_filename = 'data/result_cost_profit.json'
	firm_param = setting.baseline_firm_param
	
	cost_vec = [0, 0.3, 0.6]
	results = dict()
	reward_vec = list( np.linspace(0, 1, 15) )
	results['cost_vec'] = cost_vec
	
	for cost in cost_vec:	
		firm_param['cost'] = cost
		one_firm = firm.Firm(firm_param)
		profit_vec = []
		for reward in reward_vec:			
			profit = one_firm.get_profit(price, reward, attention, trust)
			profit_vec.append(profit)
		results[cost] = {'reward_vec': reward_vec, 'profit_vec': profit_vec}

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)




def impact_initial_adopt_prob():
	pass




if __name__ == '__main__':
	#impact_cost()
	#impact_initial_info_prob()
	impact_initial_rec_prob()

	#impact_effectiveness_reward() ## optional