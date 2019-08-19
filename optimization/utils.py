import numpy as np 
from scipy.stats import norm

graph_name = 'Facebook'
#graph_name = 'Yelp'

def action_to_key(action):
	return str(action['reward']) + ',' + str(action['price'])


######## also put some baseline settings here ########
true_delta = 0.1 # currently, do not need to estimate

# def true_rec_prob_func(price, reward):
# 	############# linear setting ##########
# 	rec_prob = 0.02 + 0.1 * reward 
# 	#######################################
# 	########### gaussian setting ##########
# 	# x = (reward-0.6)/0.1# tansformed to standard
# 	# rec_prob = norm.cdf(x) * 0.2
# 	#######################################
# 	return rec_prob

# def true_adopt_prob_func(price, reward):
# 	adopt_prob = 0.1 + 0.2 * (1-price)
# 	return adopt_prob

def true_rec_prob_func(price, reward):
	rec_prob = 0.02 + 0.36 * reward
	# rec_prob = 0.00803 + 0.0239 * reward * 2 * (reward/0.5)**2 + 0.0202 * (1-price)
	# rec_prob *= 5
	return rec_prob

def true_adopt_prob_func(price, reward):
	adopt_prob = 0.2# + 0.2 * (1-price)
	# adopt_prob = 0.0189 + 0.008406 * (1-price)
	# adopt_prob *= 5
	return adopt_prob


possible_reward = [0, 0.5]
possible_price = [1]
possible_actions = []

for reward in possible_reward:
	for price in possible_price:
		possible_actions.append({'reward': reward, 'price': price})

### the mixed strategies only consider the mixing of two strategies
mixed_actions = [{'reward': 0, 'price': 1}, {'reward': 0.5, 'price': 1}]


possible_strategies = []
for p in np.linspace(0, 1, 11):
	possible_strategies.append([p, 1-p])

