# find a parameter setting, so that all three parties get benefits from social recommendation

import json
import firm
import setting

attention = 1
trust = 1 # when gamma=1, the trust has no impacts
#eta = 0.5

def summary_one_firm(firm_param):
	one_firm = firm.Firm(firm_param)

	############# baseline ###############
	baseline_profit, baseline_price, baseline_social_value = one_firm.get_baseline(attention, trust)

	############# optimal ################
	one_firm.opt_strategy(attention, trust)

	rec_prob_FriRec_type, rec_prob_OthInf_type = one_firm.get_rec_prob(one_firm.opt_price, one_firm.opt_reward, trust)
	adopt_prob_type = one_firm.get_adopt_prob(one_firm.opt_price, one_firm.opt_reward, trust)

	print ('baseline price:', baseline_price, 'optimal price:', one_firm.opt_price)
	print ('optimal reward:', one_firm.opt_reward)
	print ('baseline profit:', baseline_profit, 'optimal profit:', one_firm.opt_profit)
	print ('rec_prob at optimal:', rec_prob_FriRec_type)
	print ('adopt_prob at optimal:', adopt_prob_type)


if __name__ == '__main__':
	firm_param = setting.baseline_firm_param

	rec_prob = 0.02
	adopt_prob = 0.05

	firm_param['rec_prob_FriRec_type'] = {'zero': 0, 'small': rec_prob, 'large': rec_prob}
	firm_param['adopt_prob_type'] = {'zero': adopt_prob, 'small': adopt_prob, 'large': adopt_prob}

	summary_one_firm(firm_param)
