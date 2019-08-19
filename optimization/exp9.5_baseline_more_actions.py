''' consider more actions of the firm, i.e., reward to be in [0.1, ..., 0.5]
'''

import baseline_fixed_action
import utils
import numpy as np

reward_vec = np.linspace(0, 0.5, 11)

# since for mixed-strategy, we only consider two candidate actions, so adding more actions only affects the optimal fixed strategy
def rec_prob_func_gen(power):
	def rec_prob_func(price, reward):
		rec_prob = 0.02 + 0.36 * reward * (reward/0.5)**power
		return rec_prob
	return rec_prob_func


if __name__ == '__main__':
	# set the possible_reward
	utils.possible_reward = reward_vec

	opt_profit_vec = []
	for power in range(5, 11):#[5, 10]:
		print ('power:', power)
		rec_prob_func = rec_prob_func_gen(power)
		opt_action, opt_profit = baseline_fixed_action.find_opt_action(utils.true_delta, rec_prob_func, utils.true_adopt_prob_func)
		opt_profit_vec.append(opt_profit)

	print (opt_profit_vec)

