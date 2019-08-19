''' this kind of firms will not increase the price, they will only offer rewards to recommenders
'''

import firm
import setting
import numpy as np

class GoodFirm(firm.Firm):
	def opt_strategy(self, attention, trust, eta=None):
		_, baseline_price, _ = self.get_baseline(attention, trust, eta)
		opt_reward = None
		opt_profit = -np.inf
		profit_vec = []
		reward_vec = np.linspace(0, 2, firm.N_GRID)

		price = baseline_price
		for reward in reward_vec:
			if eta:
				effective_reward = reward + eta * (setting.BASELINE_PRICE - price)
			else:
				effective_reward = reward

			effective_reward *= setting.effective_reward_scale
			_profit = self.get_profit(price, reward, attention, trust, effective_reward)
			profit_vec.append(_profit)
			if _profit > opt_profit:
				opt_profit = _profit
				opt_reward = reward
		return opt_reward, opt_profit

if __name__ == '__main__':
	firm_param = {
		'other_info_prob': 0.001, # consider the scaling for state OthInf
		'rec_prob_FriRec_type': {'zero': 0, 'small': 0.06, 'large': 0.03},
		'adopt_prob_type': {'zero': 0, 'small': 0.02, 'large': 0.02}, # no difference between different types
		'gamma': 1, # a number in [0,1]
		'cost': 0,
		'old_reward': 0,
		'old_price': 1
	}

	one_firm = GoodFirm(firm_param)
	attention = 1
	trust = 0
	print (one_firm.opt_strategy(attention, trust, 0.6))
