## saves a lot of time!!!

import os
import json
import sys
import setting
import numpy as np
from scipy.stats import binom
import time
import estimation

informed_prob_fileprefix = 'data/uniform_informed_prob_'
sampling_output_filename = '/newpar/Data/social_recommend/sampling_output_zero_small_large.json'


Types = setting.Types
N_node_type = setting.N_node_type

############## params in estimation
N_STD = 10
N_CENTRAL = 200 # number of samples in [-N_STD*std+mean, +N_STD*std+mean]
N_TAIL = 100

def estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec):
	occupation_prob = recommend_prob_FriRec
	if occupation_prob['small'] == 0 and occupation_prob['large'] == 0:
		prob_FriRec_type = {'small': 0, 'large': 0}
	else:
		# the prob. to recommend increase proportionally
		initial_prob = other_info_prob * recommend_prob_OthInf['small'] / recommend_prob_FriRec['small'] 
		prob_FriRec_type = estimating(initial_prob, occupation_prob, N_node_type)
		
	prob_OthInf_type = {}
	for Type in Types:
		#prob_FriRec_type[Type] *= 1 - frac_zero_degree # since we only store the samples with non-zero degree of v
		prob_OthInf_type[Type] = (1-prob_FriRec_type[Type]) * other_info_prob
	return prob_FriRec_type, prob_OthInf_type

def get_average_informed_prob(initial_prob, N_node, N_samples): # given the size of RRset
	''' 
	pre-compute the prob. for different types of users
	to be informed by FriRec when n small degree users are occupied 
	'''
	if setting.informed_prob_average != None:
		return setting.informed_prob_average

	#initial_prob = round(np.asscalar(initial_prob), 5)

	informed_prob_filename = informed_prob_fileprefix + "{:.9f}".format(initial_prob).rstrip('0').rstrip('.')#str(initial_prob)
	if os.path.isfile(informed_prob_filename):
		print ('file exists, skip.')
		setting.informed_prob_average = json.load(open(informed_prob_filename))
		return setting.informed_prob_average

	print ('!!!!!! storing the average informed prob...')
	print ('the file name is:', informed_prob_filename)

	prob_vec = estimation.get_prob_table(initial_prob, N_node)

	count = dict()

	# different for different types
	informed_prob_sum = {}
	sample_count = {}
	for Type in Types:
		informed_prob_sum[Type] = np.array( [0.0] * (N_node_type['small']+1) )
		sample_count[Type] = np.array( [0] * (N_node_type['small']+1) )

	count_line = 0
	for line in open(sampling_output_filename):
		count_line += 1
		if count_line % 100 == 0:
			print ('count_line:', count_line)
		if count_line > N_samples: # only use a limited number of samples
			break

		data = json.loads(line)
		value_vec = data['value_vec']
		degree_vec = data['type_vec']
		degree_node_v = data['type_node_v']
		if degree_node_v == 0:
			continue #samples whose v has zero degree
		type_node_v = setting.type_of_node(degree_node_v)

		for Type in setting.Types:
			count[Type] = 0

		for idx in range(len(degree_vec)):
			degree = degree_vec[idx]
			Type = setting.type_of_node(degree)
			count[Type] += 1

			RRset_size = value_vec[idx]

			informed_prob = prob_vec[RRset_size]
			informed_prob_sum[type_node_v][ count['small'] ] += informed_prob 
			sample_count[type_node_v][ count['small'] ] += 1

	informed_prob_average = {}
	for Type in Types:
		informed_prob_average[Type] = list( informed_prob_sum[Type] / sample_count[Type] ) #element-wise division, convert to list
	with open(informed_prob_filename, 'w') as output_file:
		json.dump( informed_prob_average, output_file )

	return informed_prob_average


'''
input: 
	1. the diffusion parameters
	2. the samples containing the size of RRset, and the number of different types of users
output:
	1. the estimated prob. for one to be informed from recommendation
	2. the estimated prob. for one to be informed from other information
'''
# REVISED DONE: we need to change the return value to the prob. for different types
def estimating(initial_prob, occupation_prob_type, N_node_type, N_samples=100):
	# N_samples is the largest number of samples (lines) allowed
	#print ('initial_prob:', initial_prob, 'occupation_prob_type:', occupation_prob_type)
	N_node = N_node_type['zero'] + N_node_type['small'] + N_node_type['large']
	
	informed_prob_average = get_average_informed_prob(initial_prob, N_node, N_samples)

	start_time = time.time()

	# only on the type small
	binom_rv = binom(N_node_type['small'], occupation_prob_type['small'])
	mean = N_node_type['small'] * occupation_prob_type['small']
	std = np.sqrt( N_node_type['small'] * occupation_prob_type['small'] * (1-occupation_prob_type['small']) )
	lower_bound = max(0, int(mean - N_STD * std)-1)
	upper_bound = min(N_node_type['small'], int(mean + N_STD * std)+1)

	sum_weighted_value = dict()
	sum_config_prob = dict()
	for Type in Types:
		sum_weighted_value[Type] = 0.0
		sum_config_prob[Type] = 0.0
	
	list_tail = list(np.random.choice(N_node_type['small'], 10))
	list_central = list(np.random.choice(range(lower_bound, upper_bound), N_CENTRAL))
	#print (list_central, list_tail)
	indices = list_central + list_tail
	for i in indices: # i is the number of occupied "small"-nodes
		#print (i)
		config_prob = binom_rv.pmf(i)
		for Type in Types:
			sum_weighted_value[Type] += informed_prob_average[Type][i] * config_prob
			sum_config_prob[Type] += config_prob

	#print ('execution time:', time.time()-start_time )
	estimation_type = dict()
	for Type in Types:
		estimation_type[Type] = sum_weighted_value[Type] / sum_config_prob[Type]
	return estimation_type