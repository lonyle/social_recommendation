import os
import json
import sys
import setting
import numpy as np
from scipy.stats import binom
import time
import pymongo
from pymongo import MongoClient
import pprint as pp

import matplotlib.pyplot as plt

############## params in estimation
N_STD = 10
N_CENTRAL = 20 # number of samples in [-N_STD*std+mean, +N_STD*std+mean]
MAX_SAMPLES = 1000 # the maximum number of samples for a n_node

'''
the format of a sample (as input) is 
{
	'value_vec': value_vec, 'type_vec': type_vec, 'type_node_v': type_node_v
}
'''

# goal: estimate the quantity of interest (the probability for a node to be informed from recommendation or other sources)

Types = setting.Types
N_node_type = setting.N_node_type
frac_zero_degree = setting.frac_zero_degree

# return the probability for different types of users to be informed
def estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec):
	initial_prob = other_info_prob * recommend_prob_OthInf['small'] / recommend_prob_FriRec['small'] # the prob. to recommend increase proportionally
	occupation_prob = recommend_prob_FriRec
	prob_FriRec_type = estimating_mongodb(initial_prob, occupation_prob, N_node_type)
	prob_OthInf_type = {}
	for Type in Types:
		#prob_FriRec_type[Type] *= 1 - frac_zero_degree # since we only store the samples with non-zero degree of v
		prob_OthInf_type[Type] = (1-prob_FriRec_type[Type]) * other_info_prob
	return prob_FriRec_type, prob_OthInf_type

''' the key to estimation: the probability to be informed from other friends' recommendations '''
def get_prob_table(initial_prob, MAX):
	print ('computing the probability table...')
	prob_vec = [] # prob_vec[n]: the probability to be percolated in a cluster of n nodes
	mult = 1
	for n in range(MAX+1):
		prob = 1 - mult
		mult *= (1-initial_prob)
		prob_vec.append(prob)
	print ('computing done.')
	return prob_vec



''' the estimated probability for a user to be in state FriRec, for different types'''
def estimating_mongodb(initial_prob, occupation_prob_type, N_node_type, N_samples=1000):
	print ('initial_prob:', initial_prob, 'occupation_prob_type:', occupation_prob_type)

	# connect to the database
	client = MongoClient()
	db = client.sample_database
	samples = db.samples

	N_node = N_node_type['zero'] + N_node_type['small'] + N_node_type['large']

	start_time = time.time()

	prob_vec = get_prob_table(initial_prob, N_node)

	lower_bound = 0
	upper_bound = 0
	for Type in Types:
		mean = N_node_type[Type] * occupation_prob_type[Type]
		std = np.sqrt( N_node_type[Type] * occupation_prob_type[Type] * (1-occupation_prob_type[Type]) )
		lower_bound += mean - N_STD * std
		upper_bound += mean + N_STD * std

	lower_bound = max(0, int(lower_bound))
	upper_bound = min(N_node, int(upper_bound))
	print ('lower_bound:', lower_bound, 'upper_bound:', upper_bound)

	### 1. different sample, use different indices
	# for n_sample in range(N_samples):
	# 	if n_sample % 50 == 0:
	# 		print (n_sample)
	# 	list_tail = list(np.random.choice(N_node, 10))
	# 	list_central = list(np.random.choice(range(lower_bound, upper_bound), 40))
	# 	#print (list_central, list_tail)
	# 	indices = list_central + list_tail
	# 	for i in indices:
	# 		#print ('n_sample:', n_sample, 'i:', i)
	# 		one_sample = samples.find_one({"$and": [{'n_sample': int(n_sample)}, {'n_node': int(i)}]})
	# 		config_prob = get_config_prob(one_sample['n_node_type'], occupation_prob_type, N_node_type)
	# 		sum_weighted_value += prob_vec[one_sample['value']] * config_prob
	# 		sum_prob += config_prob
	##############################################

	### 2. use the same indices for different samples
	#samples.create_index([('n_node', 1)]) # create index if not exist

	binom_rv_type = dict()
	for Type in Types:
		print (Type, 'N_node_type:', N_node_type[Type], 'occupation_prob_type:', occupation_prob_type[Type])
		binom_rv_type[Type] = binom(N_node_type[Type], occupation_prob_type[Type])

	list_tail = []#list(np.random.choice(N_node, 20))
	list_central = list(np.random.choice(range(lower_bound, upper_bound), N_CENTRAL))
	indices = list_central + list_tail
	estimation_type = {}
	for Type in setting.Types:
		print ('Type:', Type)
		sum_weighted_value = 0.0
		sum_prob = 0.0
		for i in indices:
			print ('n_node:', i)

			sample_cur = samples.find({'n_node': int(i), 'type_node_v': Type}) # Type is the type of the focused node v

			N_sample = sample_cur.count()
			print ('N_sample in the database:', N_sample)
			retain_prob = min(1, MAX_SAMPLES / N_sample)
			print ('retain_prob:', retain_prob)
			#print ('number of samples in type ' + Type +':', sample_cur.count())
			count_sample = 0
			for one_sample in sample_cur:
				count_sample += 1
				if count_sample > MAX_SAMPLES:
					break
				
				#begin_time = time.time()
				config_prob = get_config_prob(one_sample['n_node_type'], binom_rv_type)
				#print ('execution time:', time.time()-begin_time)

				# if Type == 'medium':
				# 	print ('value:', one_sample['value'], 'config_prob:', config_prob)
				sum_weighted_value += prob_vec[one_sample['value']] * config_prob
				#print ('value of the sample:', one_sample['value'])
				#print ('config_prob:', config_prob)
				sum_prob += config_prob
		#print ('sum_weighted_value:', sum_weighted_value)
		#print ('sum_prob:', sum_prob)
		estimation_type[Type] = sum_weighted_value / sum_prob

	##############################################
	print ('execution time:', time.time()-start_time )
	return estimation_type

# calculate the probability to observe a certain configuration
def get_config_prob(type_count, binom_rv_type):
	# different nodes might have different occupation_prob
	#print ('type_count', type_count)
	prob = 1
	type_count_dict = {'small': type_count[1], 'large': type_count[2]}
	for Type in Types:
		# maybe slow to construct so many r.v. (optimized)
		#binom_rv = binom(N_node_type[Type], occupation_prob_type[Type])
		binom_pmf = binom_rv_type[Type].pmf( type_count_dict[Type] )
		#print (binom_pmf)
		prob *= binom_pmf
		#print ('binom_pmf:', binom_pmf)
	return prob

if __name__ == '__main__':
	initial_prob = 0.001
	occupation_prob_type = {'small': 0.05, 'medium': 0.15, 'large': 0.1}
	est = estimating_mongodb(initial_prob, occupation_prob_type, N_node_type)
	print ('the estimated prob. to be in FriRec for each type:', est)
	# 1. {'medium': 0.00021032079158899745, 'small': 3.1609319827615247e-05, 'large': 0.0022609898787319918}
	# 2. new seeting * 10:  {'large': 0.75136012421622889, 'medium': 0.32922314330842151, 'small': 0.099172673835271827}