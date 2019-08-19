''' this experiment is to compare the running time of the naive algorithm and the accelarated simulation algorithm
	1. running time of naive sampling algorithm
	2. running time of the improved algorithm
'''


import sampling
import estimation_uniform
import simulation

import sys
sys.path.insert(0, 'preprocess')
import osn
import numpy as np

import time
import json

def time_RRset(graph,
			   other_info_prob,
			   recommend_prob_OthInf,
			   recommend_prob_FriRec):
	print ('running RRset...')
	# preprocessing params
	occupation_prob = recommend_prob_FriRec
	if occupation_prob['small'] == 0 and occupation_prob['large'] == 0:
		return 0 # do not need to calculate
	else:
		# the prob. to recommend increase proportionally
		initial_prob = other_info_prob * recommend_prob_OthInf['small'] / recommend_prob_FriRec['small'] 
		
	# start running the simulation
	begin_time = time.time()
	est_vec = []
	for epoch in range(1): # each epoch we run 100 simulations
		est_small = sampling.get_est_informed_prob(graph, initial_prob, occupation_prob, 'small')
		est_large = sampling.get_est_informed_prob(graph, initial_prob, occupation_prob, 'large')
		est_vec.append(est_large)

	running_time = time.time() - begin_time
	print ('time RRset:', running_time)
	print ('the estimated value:', np.average(est_vec))
	return running_time

def time_uniform(other_info_prob,
				 recommend_prob_OthInf,
				 recommend_prob_FriRec):
	# the graph is default, so we don't need the graph parameter
	print ('running uniform...')
	begin_time = time.time()
	prob_FriRec, prob_OthInf = estimation_uniform.estimate_informed_prob(
			other_info_prob, 
			recommend_prob_OthInf, 
			recommend_prob_FriRec)
	running_time = time.time() - begin_time
	print ('time pre-computed:', running_time)
	print ('prob_FriRec_type:', prob_FriRec)
	return running_time

def time_agent_based(graph,
					 other_info_prob,
					 recommend_prob_OthInf,
					 recommend_prob_FriRec):
	print ('running agent based...')
	begin_time = time.time()
	
	with_prob = recommend_prob_FriRec['small'] # we just choose the small nodes
	without_prob = other_info_prob * with_prob

	for epoch in range(2000): # each epoch we get 1 sample
		print ('agent-based simulation: sample', epoch)
		simulation.diffusion_scale(graph, without_prob, with_prob)

	running_time = time.time() - begin_time
	print ('time agent-based:', running_time)
	return running_time

firm_param = {
	'other_info_prob': 0.1, # consider the scaling for state OthInf
	'rec_prob_FriRec_type': {'zero': 0, 'small': 0.033, 'large': 0.0198},
	'adopt_prob_type': {'zero': 0.2, 'small': 0.2, 'large': 0.2}, # no difference between different types, original: 0.2
	'gamma': 1, # a number in [0,1]
	'cost': 0,
	'old_reward': 0,
	'old_price': 1
}

def one_experiment(graph, other_info_prob, recommend_prob_FriRec):
	recommend_prob_OthInf = recommend_prob_FriRec # just keep the same

	running_time_dict = dict()

	running_time_dict['agent_based'] = time_agent_based(graph, other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)
	running_time_dict['uniform'] = time_uniform(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)
	running_time_dict['RRset'] = time_RRset(graph, other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)

	print (running_time_dict)
	return running_time_dict

output_filename = 'data/exp_timing.json'

if __name__ == '__main__':
	graph = osn.OnlineSocialNetwork('yelp')

	running_time_dict_vec = []

	for other_info_prob in [0.001, 0.01, 0.1, 0.4]:
		running_time_dict = one_experiment(graph, 
								other_info_prob,
								firm_param['rec_prob_FriRec_type'])
		running_time_dict_vec.append(running_time_dict)

	for rec_prob_scale in [0.2, 0.5, 1, 1.5]:
		recommend_prob_FriRec = {'zero': 0,
								 'small': firm_param['rec_prob_FriRec_type']['small']*rec_prob_scale,
								 'large': firm_param['rec_prob_FriRec_type']['large']*rec_prob_scale}
		running_time_dict = one_experiment(graph, 
								firm_param['other_info_prob'],
								recommend_prob_FriRec)
		running_time_dict_vec.append(running_time_dict)

	print (running_time_dict_vec)
	with open(output_filename, 'w') as output_file:
		json.dump(running_time_dict_vec, output_file, indent=4)

	
