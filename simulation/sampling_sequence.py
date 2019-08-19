# store the sampling results in mongodb, with heterogeneous types
# the value is the size of the RRset, where the RRset does not include the selected node
'''
the output format of a sample is
{
	'value_vec': value_vec, 'type_vec': type_vec, 'type_node_v': type_node_v
}
'''
import numpy as np 
from scipy.stats import binom
from scipy.stats import norm
import json

import sys
sys.path.insert(0, 'preprocess')
import osn

import matplotlib.pyplot as plt
import time
import setting

import pymongo
from pymongo import MongoClient

occupation_scale = setting.occupation_scale

# output: a sequence of values, and a sequence of nodes' types
# in the following function, the value of interest is the size of reverse reachable set
def get_sequence_samples(graph):
	v = np.random.choice(list(graph.nodes)) # v is the first chosen node
	if graph.is_weighted == False:
		type_node_v = len(graph.edges[v]) # the type is the degree
	else: # weighted graph generate random graph
		type_node_v = len(graph.weighted_edges[v])
		# !!!! important !!!! randomly retain edges
		graph.get_random_edges_by_weight()

	# revised on 2018-08-10: select nodes from different types, each type has different prob
	x = np.inf
	for Type in setting.Types:
		if occupation_scale[Type] != 0:
			x = min(x, 1 / occupation_scale[Type]) # make sure enough node to choose for each type
	shuffle_node_vec = []
	# from each type, select some nodes, this include the previously chosen node v
	for Type in setting.Types:
		N_selected = int(x*occupation_scale[Type] * len(graph.nodes_type[Type]))
		node_vec = list( np.random.choice(graph.nodes_type[Type], N_selected, replace=False) )
		shuffle_node_vec += node_vec
	##### original version ######
	#shuffle_node_vec = list(graph.nodes)
	#############################
	np.random.shuffle(shuffle_node_vec)
	
	print ('Number of neighbors of v:', type_node_v)
	if type_node_v == 0: # shortcut
		type_vec = [] #[-1] * len(shuffle_node_vec)
		value_vec = [] #[0] * len(shuffle_node_vec)
		return value_vec, type_vec, type_node_v

	value_vec = []
	type_vec = [] # now, three types: small/medium/large, the type of each visited node

	## initialize awaiting_flag: awaiting to be added to the cluster
	awaiting_flag = dict()
	for node in graph.nodes:
		awaiting_flag[node] = False

	## initialize RRset and potential_RRset
	RRset = set()
	potential_RRset = set() #once activated, should be in the RRset
	# the initial potential_RRset is v's incoming neighbors
	for v_neighbor in graph.edges[v]:
		potential_RRset.add(v_neighbor)

	## get a sequence of samples
	node_count = 0
	for node in shuffle_node_vec:
		node_count += 1
		if node_count % 100000 == 0:
			print (node_count)
		if node == v: # we do not consider the recommendations from node v, because it is not "from others"
			continue
		awaiting_flag[node] = True
		neighbors = graph.edges[node]

		## get the type of the node
		N_neighbors = len(neighbors)
		
		type_vec.append(N_neighbors)

		## get the size of RRset
		current_nodes = [] # the new sources of diffusion
		# check whether the node should be in RRset
		if node in potential_RRset:
			current_nodes = [node]
				
		# diffusion to other nodes
		while len(current_nodes) > 0:
			# the new nodes are added in the RRset, so these nodes will not be in the awaiting set
			for node_ in current_nodes:
				RRset.add(node_)
				awaiting_flag[node_] = False

			new_nodes = []
			for node_ in current_nodes:
				neighbors_ = graph.edges[node_]
				for neighbor_ in neighbors_: # these nodes are potential_RRset
					if neighbor_ in awaiting_flag: # check the existence of key
						if awaiting_flag[neighbor_] == True:
							new_nodes.append(neighbor_)
						else:
							potential_RRset.add(neighbor_)
			current_nodes = new_nodes[:]
			
		value_vec.append(len(RRset))
	return value_vec, type_vec, type_node_v

def mongodb_change_index():
	client = MongoClient()
	db = client.sample_database
	samples = db.samples
	samples.drop_index([('n_node', 1)])
	samples.create_index([('n_sample',1), ('n_node',1)])

# store the results into the mongodb from the files
# !!! generate the count of types
# !!! only store the samples with non-zero degree
def store_mongodb(sampling_output_filename, N_samples=2000):
	input_file = open(sampling_output_filename)
	client = MongoClient()
	print ('dropping existing database...')
	client.drop_database('sample_database')
	print ('dropping completed.')
	db = client.sample_database # create a database
	samples = db.samples # create a collection
	

	count = dict()
	n_sample = 0
	
	for line in input_file:
		if n_sample % 1 == 0:
			print (n_sample)
		if n_sample > N_samples:
			break

		data = json.loads(line)
		value_vec = data['value_vec']
		degree_vec = data['type_vec']
		degree_node_v = data['type_node_v']
		if degree_node_v == 0:
			continue # do not store the samples whose v has zero degree

		type_node_v = setting.type_of_node(degree_node_v)
		
		for Type in setting.Types:
			count[Type] = 0

		sample_vec = []		
		for idx in range(len(degree_vec)):
			degree = degree_vec[idx]
			Type = setting.type_of_node(degree)

			count[Type] += 1

			n_node_type = [count['zero'], count['small'], count['large']]
			one_sample = {
				'n_sample': n_sample, # the idx of samples (each sample corresponds to a sequence)
				'n_node': idx+1, # the number of occupied nodes,
				'n_node_type': n_node_type, # the number of occupied nodes of each type, should sum to 'n_node'
				'value': value_vec[idx], # the size of RRset
				'type_node_v': type_node_v
			}
			#print (one_sample)
			sample_vec.append(one_sample)

		samples.insert_many(sample_vec)
		n_sample += 1

	input_file.close()

	samples.create_index([('n_node',1), ('type_node_v',1)])
	return 0

def store_sampling_results(graph, output_filename, N_sample=2000):
	f_output = open(output_filename, 'w')
	for n in range(N_sample):
		print ('sample', n)
		value_vec, type_vec, type_node_v = get_sequence_samples(graph) # store the results
		data = {'value_vec': value_vec, 'type_vec': type_vec, 'type_node_v': type_node_v}
		f_output.write(json.dumps(data) + '\n')
		if len (value_vec) > 0:
			print ('size of the largest RRset', value_vec[-1])
		# plt.plot(np.arange(len(size_vec)), size_vec)
		# plt.show()
	f_output.close()
	return 0

if __name__ == '__main__':	
	sampling_output_filename = '/newpar/Data/social_recommend/sampling_output_zero_small_large_0.7.json'

	# step 1: get samples
	graph = osn.OnlineSocialNetwork('yelp')
	store_sampling_results(graph, sampling_output_filename)

	# step 2: insert to mongodb
	#store_mongodb(sampling_output_filename)
	#mongodb_change_index()

