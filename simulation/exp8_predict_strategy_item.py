# in the item-specific level, do simulation and predict the optimal reward/price

# the only unkown is adopt_prob_type (click_rate * 1/10)
import print_one_firm

def strategy(item):
	# we currently only 6 parameters
	p_non_receiver = item['p_non_receiver']
	p_receiver = item['p_receivers']
	
	old_price = item['old_price']
	old_reward = item['old_reward']

	p_adopt = item['click_rate'] * item['click_to_adopt_ratio']

	firm_param = {
		'other_info_prob': p_non_receiver / p_receiver,
		'rec_prob_FriRec_type': {'zero': 0, 'small': p_receiver, 'large': p_receiver},
		'adopt_prob_type': {'zero': p_adopt, 'small': p_adopt, 'large': p_adopt},
		'gamma': 1,
		'cost': 0,
		'old_reward': old_reward,
		'old_price': old_price
	}

	print_one_firm.summary_one_firm(firm_param)

if __name__ == '__main__':
	item = {
		'name': 'yanxuan',
		'p_non_receiver': 6.40704 * 10**(-7),
		'p_receivers': 0.040576,
		'click_rate': 0.069682,
		'click_to_adopt_ratio': 1,
		'old_price': 0.8,
		'old_reward': 0.5
	}
	item_vec = [item]# load from file
	for item in item_vec:
		print ('######## item name:', item['name'])
		strategy(item)


