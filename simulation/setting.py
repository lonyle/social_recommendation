import numpy as np
import sys
sys.path.insert(1, 'inference')
import regression

####### global variable, in memory
informed_prob_average = None 
######

UNIFORM = True

frac_zero_degree = 0.42688528 #yelp

Types = ['small', 'large']

occupation_scale = {'zero': 0.0, 'small': 0.006621015582774402, 'large': 0.003970798129286127} # the scale of recommendation probability, TODO

N_node_type = {'zero': 566093, 'small': 748378, 'large': 11630}

old_trust = 0

BASELINE_PRICE = 1

effective_reward_scale = 1 # for experiment, this parameter is the effective reward to get the probability of adoption and recommendations. 
# E.g. when eta>0, the social value is added to effective reward

baseline_firm_param = {
	'other_info_prob': 0.1, # consider the scaling for state OthInf
	'rec_prob_FriRec_type': {'zero': 0, 'small': 0.033, 'large': 0.0198},
	'adopt_prob_type': {'zero': 0.2, 'small': 0.2, 'large': 0.2}, # no difference between different types, original: 0.2
	'gamma': 1, # a number in [0,1]
	'cost': 0,
	'old_reward': 0,
	'old_price': 1
}

N_GRID = 41 # for the grid search

def type_of_node(degree):
	if degree == 0:
		Type = 'zero'
	elif degree < 500:
		Type = "small"
	# elif degree < 1200:
	# 	Type = "medium"
	else:
		Type = "large"
	return Type