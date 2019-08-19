# all users have the same recommendation prob.

import numpy as np 
from scipy.stats import binom
from scipy.stats import norm
import sampling
import json
import osn
import matplotlib.pyplot as plt
import time
import os
import simulation_setting

sampling_result_filename = '/newpar/Data/output_sampling.json'
S_result_fileprefix = 'data/output_S_'

# TODO: not only record the size, but also record the details of every kind of nodes.

def get_random_RRset_size(graph):
	print ('Number of users:', len(graph.nodes))
	v = np.random.choice(list(graph.nodes)) # v is the first chosen node
	shuffle_node_vec = list(graph.nodes)
	np.random.shuffle(shuffle_node_vec)
	RRset = set()
	print ('Number of neighbors of v:', len(graph.edges[v]))
	if len(graph.edges[v]) == 0: # shortcut
		return [1] * (len(graph.nodes)-1)

	size_vec = []
	## initialize awaiting_flag: awaiting to be added to the cluster
	awaiting_flag = dict()
	for node in graph.nodes:
		awaiting_flag[node] = False
	####
	count = 0
	for node in shuffle_node_vec:
		# count += 1
		# if count % 10000 == 0:
		# 	print (count)
		if node == v:
			continue
		awaiting_flag[node] = True
		neighbors = graph.edges[node]

		current_nodes = []
		# check whether a node is in RRset
		for neighbor in neighbors:
			if neighbor in RRset or neighbor == v: # new node will be added
				#RRset.add(node)
				current_nodes = [node]
				break
		
		# diffusion to other nodes
		while len(current_nodes) > 0:
			# the new nodes are added in the RRset, so these nodes will not be in the awaiting set
			for node_ in current_nodes:
				RRset.add(node_)
				awaiting_flag[node_] = False

			new_nodes = []
			for node_ in current_nodes:
				neighbors_ = graph.edges[node_]
				for neighbor_ in neighbors_:
					if neighbor_ in awaiting_flag: # check the existence of key
						if awaiting_flag[neighbor_] == True:
							new_nodes.append(neighbor_)
			current_nodes = new_nodes[:]
			
		size_vec.append(len(RRset))
	return size_vec

def store_sampling_results(graph, N_sample=1000):
	f_output = open(sampling_result_filename, 'a')
	for n in range(N_sample):
		print ('sample', n)
		size_vec = get_random_RRset_size(graph) # store the results
		f_output.write(json.dumps(size_vec) + '\n')
		print ('size of the largest RRset', size_vec[-1])
		# plt.plot(np.arange(len(size_vec)), size_vec)
		# plt.show()
	return 0

def get_S(initial_prob): # probability for an node to adopt given r nodes are occupied
	S_result_filename = S_result_fileprefix + str(initial_prob)
	if os.path.isfile(S_result_filename):
		S_average = json.load(open(S_result_filename))
		return S_average

	print ('storing the average prob of being informed (uniform)')
	f = open(sampling_result_filename)

	line = f.readline()
	size_vec = json.loads(line)
	N_node = len(size_vec) + 1
	prob_vec = sampling.get_prob_table(initial_prob, N_node)

	# calculate the average vector on the fly
	S_sum = np.array( [0.0] * (N_node-1) )
	S_count = 0
	while line:
		S_count += 1
		if S_count % 100 == 0:
			print (S_count)
		size_vec = json.loads(line)
		S_vec = np.array(list(map(lambda x: prob_vec[x], size_vec))) # -1 because that the inconsistency of "influenced" and "occupied"
		S_sum += S_vec

		line = f.readline()		
	
	S_average = S_sum / S_count
	with open(S_result_filename, 'w') as output_file:
		json.dump(list(S_average), output_file)

	print ('done.')

	return S_average

'''get the estimated probability for a user to be informed'''
def get_expected_size(initial_prob, occupation_prob): # phi is the percolation probability
	#print ('initial_prob:', initial_prob, 'occupation_prob:', occupation_prob)
	S = get_S(initial_prob)
	start_time = time.time()
	N_node = len(S)
	sum_ = 0
	# normal distribution with mean np and variance np(1-p)
	binom_rv = binom(N_node, occupation_prob)
	mean = N_node * occupation_prob
	std = np.sqrt( N_node * occupation_prob * (1-occupation_prob) )
	# for r in range(N_node):
	# 	sum_ += S[r] * (norm.cdf((r-mean)/std)- norm.cdf((r-1-mean)/std) )
	for r in range(max(0, int(mean-10*std)), min(N_node,int(mean+10*std)+1) ):
		sum_ += S[r] * binom_rv.pmf(r)
	#print ('running time', time.time() - start_time, '(s)')
	return sum_

def get_expected_profit(without_prob_baseline, with_prob_baseline, stars, reward):
	enhancement = simulation_setting.recommend_prob_enhancement(stars, reward)
	occupation_prob = with_prob_baseline * enhancement #the probability
	initial_prob = without_prob_baseline / with_prob_baseline
	recommended_prob = get_expected_size(initial_prob, occupation_prob)
	#print ('recommended_prob:', recommended_prob)
	recommendation_amount = recommended_prob * occupation_prob + (1-recommended_prob) * without_prob_baseline * enhancement
	normalized_sales_amount = recommendation_amount / enhancement
	recommend_prob = simulation_setting.orig_recommend_prob * enhancement
	unit_profit = simulation_setting.gross_profit - recommend_prob * reward
	profit = unit_profit * normalized_sales_amount
	return profit, recommended_prob



if __name__ == '__main__':
	# graph = osn.OnlineSocialNetwork('/home/liye/Data/yelp-round11/user.json')
	# store_sampling_results(graph)

	with_prob_baseline = 0.1#0.0015 # the reviewing probability with recommendation 
	without_prob_baseline = 0.00001 # the reviewing probability without recommendation
	opt_reward, opt_profit = opt_strategy(without_prob_baseline, with_prob_baseline)
	print ('opt_reward:', opt_reward, 'opt_profit:', opt_profit)

