# this is the naive simulation which simulate the diffusion process
# agent-based!!!

import json
import osn
import numpy as np 

# 1. parameter needed assumption: the recommendation probability without reward
orig_recommend_prob = 0.1
# 2. parameter needed assumption: the gross profit ratio between price and cost
gross_profit = 5 #50%, suppose the reward = 1 which is 10%

# according to the reward and stars, generate the recommendation probability.
def recommend_prob_enhancement(stars, reward): # relative enhancement
	# the simplest case: linear distribution
	baseline = -20 + 25 * stars
	after = -20 + 25 * (stars + reward)
	return after / baseline

# recommendation probability and the initial scale of adoption
# edited in 2019-05-30: change the parameters, to separate diffusion and economic stuffs
def diffusion_scale(graph, without_prob, with_prob):
	'''
		@param without_prob: the probability to recommend without recommendation from friends
		with_prob: the probability to recommend with recommendation
	'''
	# get the conductive nodes
	conductive_nodes_flag = dict()
	recommender_flag = dict()
	for user in graph.nodes:
		recommender_flag[user] = False
		if np.random.random() < with_prob:
			conductive_nodes_flag[user] = True
		else:
			conductive_nodes_flag[user] = False
	# get the initial recommenders
	initial_nodes = []
	extra_prob = without_prob / with_prob
	for user in graph.nodes:
		if conductive_nodes_flag[user] == True:
			if np.random.random() < extra_prob:
				initial_nodes.append(user)
				recommender_flag[user] = True
	# iteratively generate other users
	current_recommenders = initial_nodes[:]

	count_recommenders = 0
	while len(current_recommenders) > 0:
		count_recommenders += len(current_recommenders)
		new_recommenders = []
		for user in current_recommenders:
			friends = graph.edges[user]
			for friend in friends:
				if friend in conductive_nodes_flag.keys():
					if conductive_nodes_flag[friend] == True and recommender_flag[friend] == False:
						new_recommenders.append(friend)
						recommender_flag[friend] = True
				else:
					pass #print ('friend who is not in keys:', friend)
		current_recommenders = new_recommenders[:]

	return count_recommenders

def expected_profit(without_prob_baseline, with_prob_baseline, stars, reward, graph, N_simulations = 500):
	recommend_prob = orig_recommend_prob * recommend_prob_enhancement(stars, reward)
	unit_profit = gross_profit - reward * recommend_prob
	print ('unit_profit:', unit_profit)
	scale_vec = []
	for i in range(N_simulations):
		print ('# simulation', i)
		enhancement = recommend_prob_enhancement(stars, reward)
		with_prob = with_prob_baseline * enhancement
		without_prob = without_prob_baseline * enhancement

		count_recommenders = diffusion_scale(graph, without_prob, with_prob)
		normalized_scale = count_recommenders / enhancement # only consider comparison with the no-rewarding case 
		scale_vec.append(normalized_scale)
	print ('scale_vec:', scale_vec)
	ave_scale_adopters = np.average(scale_vec)
	print ('ave_scale:', ave_scale_adopters)

	profit = ave_scale_adopters * unit_profit
	return profit, ave_scale_adopters

def opt_strategy(without_prob_baseline, with_prob_baseline, stars, graph):
	opt_reward = None 
	opt_profit = -np.inf
	profit_vec = []
	ave_scale_vec = []
	for reward in np.linspace(0, 2, 11):
		print ('reward:', reward)
		profit, ave_scale = expected_profit(without_prob_baseline, with_prob_baseline, stars, reward, graph)
		profit_vec.append(profit)
		ave_scale_vec.append(ave_scale)
		if profit > opt_profit:
			opt_profit = profit
			opt_reward = reward
	print ('profit_vec:', profit_vec)
	print ('ave_scale_vec:', ave_scale_vec)
	return opt_reward, opt_profit

if __name__ == '__main__':
	graph = osn.OnlineSocialNetwork('yelp')

	with_prob_baseline = 0.0015 # the reviewing probability with recommendation 
	without_prob_baseline = 0.000013 # the reviewing probability without recommendation
	stars = 3.5
	opt_reward, opt_profit = opt_strategy(without_prob_baseline, with_prob_baseline, stars, graph)
	print ('opt_reward:', opt_reward, 'opt_profit:', opt_profit)